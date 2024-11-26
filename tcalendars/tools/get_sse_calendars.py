import random
import requests
import csv
import time
from moment import moment

SZSE_URL = 'http://www.szse.cn/api/report/exchange/onepersistenthour/monthList'


def get_se_dates_by_month(date):
    params = {
        'month': moment(date).format('YYYY-MM'),
        'random': random.random(),
    }
    response = requests.get(SZSE_URL, params=params)
    print(params)
    return response.json()['data']


def get_se_calendars():
    '''
    zrxh：weekday，1（星期天） - 7（星期六）
    jybz：1 - 交易日；0 - 非交易日
    jyrq：交易日期
    :return:
    '''
    dt = moment('2005-1-1')
    now = moment(moment().format('YYYY-12-31'))
    with open('se_calendar.csv', 'w') as fd:
        w = None
        for d in get_se_dates_by_month(dt):
            if w is None:
                w = csv.DictWriter(fd, fieldnames=list(d.keys()))
                w.writeheader()
            w.writerow(d)
        dt.add(1, 'months', inplace=True)
        count = 0
        while dt < now:
            for d in get_se_dates_by_month(dt):
                w.writerow(d)
            count = count + 1
            if count > 10:
                time.sleep(5 + int(random.random()*10))
                count = 0
            dt.add(1, 'months', inplace=True)


if __name__ == '__main__':
    get_se_calendars()
