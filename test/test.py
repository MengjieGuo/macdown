#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2018/1/11 上午11:25
# @Author : ScrewMan
# @Site : 
# @File : test.py
# @Software : PyCharm


import requests
import eventlet
eventlet.monkey_patch()

try:
    with eventlet.Timeout(10):
        re = requests.get('http://125.46.83.203:8888',timeout=10)
        print(re.status_code)
except Exception as e:
    print(1, e)