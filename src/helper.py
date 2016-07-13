# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time

BASE_URL = 'http://www.neeq.com.cn/'


def read_data_str(target, values):
    try:
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')  # 转换 str 为 bytes
        req = urllib.request.Request(BASE_URL + target, data)
        with urllib.request.urlopen(req) as response:
            the_page = response.read().decode()
    except:
        print("ERROR")
    if the_page:
        return the_page


def get_current_time():
    ISOTIMEFORMAT = '%Y-%m-%d'
    return time.strftime(ISOTIMEFORMAT, time.localtime())
