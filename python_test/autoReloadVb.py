#!/usr/bin/python
# # -*- coding: utf-8 -*-
from selenium import webdriver
import time
c = webdriver.Firefox()
while True:
    c.get('https://vbitex.com/Trade/index/id/5.html?l=zh-cn')
    time.sleep(600)