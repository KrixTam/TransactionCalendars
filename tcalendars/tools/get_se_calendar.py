import random
import requests
import csv
import time
from moment import moment
from os import path

SZSE_URL = 'http://www.szse.cn/api/report/exchange/onepersistenthour/monthList'


def get_dates_by_month(date):
    params = {
        'month': moment(date).format('YYYY-MM'),
        'random': random.random(),
    }
    response = requests.get(SZSE_URL, params=params)
    # print(params)
    return response.json()['data']


def get_filename(dir=None):
    output_filename = 'se_calendar.csv'
    if dir is None:
        dir_name = path.dirname(path.dirname(__file__))
    else:
        dir_name = dir
    return path.join(dir_name, output_filename)


def get_calendar(start_date='2005-1-1', end_date=None, dir=None):
    '''
    zrxh：weekday，1（星期天） - 7（星期六）
    jybz：1 - 交易日；0 - 非交易日
    jyrq：交易日期
    :return:
    '''
    print('获取A股交易日历中，请稍等……')
    dt = moment(start_date)
    if end_date is None:
        now = moment(moment().format('YYYY-12-31'))
    else:
        now = moment(end_date)
    with open(get_filename(dir), 'w') as fd:
        w = None
        for d in get_dates_by_month(dt):
            if w is None:
                w = csv.DictWriter(fd, fieldnames=list(d.keys()))
                w.writeheader()
            w.writerow(d)
        dt.add(1, 'months', inplace=True)
        count = 0
        while dt < now:
            for d in get_dates_by_month(dt):
                w.writerow(d)
            count = count + 1
            if count > 10:  # pragma: no cover
                time.sleep(4 + int(random.random()*10))
                count = 0
            dt.add(1, 'months', inplace=True)
