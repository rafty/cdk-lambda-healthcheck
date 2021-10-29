from datetime import datetime, timezone
import urllib.request
import xml.etree.ElementTree as et
from aws_lambda_powertools import Logger

logger = Logger(child=True)


def pub_date_to_utc(pub_date):
    # e.g. pub_date: Thu, 22 Aug 2019 23:40:01 PDT
    #                Thu, 08 Mar 2012 14:11:41 PST
    #                Thu, 08 Mar 2012 14:11:41 PCT

    logger.info(f'pub_date: {pub_date}')
    elements = pub_date.split(' ')

    if elements[-1] == 'PDT':
        _date = elements[1:-1]
        _date.append('-0700')
        _pub_date = ' '.join(_date)
        utc_time = datetime.strptime(_pub_date, '%d %b %Y %H:%M:%S %z'). \
            astimezone(timezone.utc)
        return utc_time
    elif elements[-1] == 'PCT' or elements[-1] == 'PST':
        _date = elements[1:-1]
        _date.append('-0800')
        _pub_date = ' '.join(_date)
        utc_time = datetime.strptime(_pub_date, '%d %b %Y %H:%M:%S %z'). \
            astimezone(timezone.utc)
        return utc_time
    else:
        raise ValueError('datetime format error: {}'.format(pub_date))


def rss_read(url):
    """
    return: item(dict) list
    item: {
       'pub_date':
          datetime.datetime(2019,8,23,11,18,35,tzinfo=datetime.timezone.utc),
       'description':
          'The majority of impaired EC2 instances and EBS...'
    }
    """
    root = et.fromstring(urllib.request.urlopen(url).read())
    items = list()
    for item in root.iter('item'):
        pub_date = pub_date_to_utc(item[2].text)
        description = item[4].text
        items.append(dict(pub_date=pub_date, description=description))

    logger.info(f'item list: {items}')
    return items
