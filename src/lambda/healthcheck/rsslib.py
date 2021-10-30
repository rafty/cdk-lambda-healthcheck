from datetime import datetime, timezone
import urllib.request
import xml.etree.ElementTree as et
from aws_lambda_powertools import Logger

logger = Logger(child=True)


def pacific_time_to_utc(pacific_time) -> datetime:
    # e.g. pacific_time: Thu, 22 Aug 2019 23:40:01 PDT
    #                    Thu, 08 Mar 2012 14:11:41 PST
    #                    Thu, 08 Mar 2012 14:11:41 PCT

    logger.debug(f'pacific_time: {pacific_time}')
    elements = pacific_time.split(' ')

    if elements[-1] == 'PDT':
        _date = elements[1:-1]
        _date.append('-0700')
        _pacific_time = ' '.join(_date)
        utc_time = datetime.strptime(_pacific_time, '%d %b %Y %H:%M:%S %z'). \
            astimezone(timezone.utc)
        return utc_time
    elif elements[-1] == 'PCT' or elements[-1] == 'PST':
        _date = elements[1:-1]
        _date.append('-0800')
        _pacific_time = ' '.join(_date)
        utc_time = datetime.strptime(_pacific_time, '%d %b %Y %H:%M:%S %z'). \
            astimezone(timezone.utc)
        return utc_time
    else:
        raise ValueError('datetime format error: {}'.format(pacific_time))


def rss_read(url, service, region) -> list:
    """
    return: list of item: dict
    item: {
       'pacific_time': datetime.datetime(2019,8,23,11,18,35,tzinfo=datetime.timezone.utc),
       'service': 'Amazon EC2',
       'region': 'ap-northeast-1',
       'description':'The majority of impaired EC2 instances and EBS...'
    }
    """
    root = et.fromstring(urllib.request.urlopen(url).read())
    items = list()
    for item in root.iter('item'):
        pacific_time = pacific_time_to_utc(item[2].text)
        description = item[4].text
        items.append(dict(pacific_time=pacific_time, description=description, service=service, region=region))

    logger.debug(f'item list: {items}')
    return items


def extract_service_error(service_list):
    extracted_status_list = []
    for service in service_list:
        service_error_status_list = rss_read(service.get('rss'), service.get('service'), service.get('region'))

        error_count = 0
        for status in service_error_status_list:
            delta = datetime.now(timezone.utc) - status['pacific_time']
            # if delta.total_seconds() <= (((5 * 60) * 2) * 6) * 24 * 100: # for test
            if delta.total_seconds() <= (5 * 60) * 2:  # 5 min(Polling interval) x 2
                extracted_status_list.append(status)
                error_count += 1

        if not error_count:
            extracted_status_list.append(
                dict(description='Normal',
                     pacific_time=datetime.now(timezone.utc),
                     service=service.get('service'),
                     region=service.get('region')))

    return extracted_status_list
