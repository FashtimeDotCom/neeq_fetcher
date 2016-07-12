# -*- coding: utf-8 -*-
import urllib.request
import urllib.error

baseURL = 'http://www.neeq.com.cn/'


def read_data_str(target, values):
    try:
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')  # data should be bytes
        req = urllib.request.Request(baseURL + target, data)
        with urllib.request.urlopen(req) as response:
            the_page = response.read().decode()
    except:
        print("ERROR")
    if the_page:
        return the_page
