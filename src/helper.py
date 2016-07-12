# -*- coding: utf-8 -*-
import urllib.request
import urllib.error

baseURL = 'http://www.neeq.com.cn/'


def read_data_str(target):
    try:
        response = urllib.request.urlopen(baseURL + target)
        html = response.read()
        data_str = html.decode()
        return data_str
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        return None
