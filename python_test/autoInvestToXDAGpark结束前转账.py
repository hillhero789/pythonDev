#!/usr/bin/python
# # -*- coding: utf-8 -*-
from selenium import webdriver
import time
import datetime
import os
c = webdriver.Firefox()
lastRound = 0
doOnce = True
countDownTime = 0
while True:
    c.get('http://fomoxdag.xdagpark.com/')
    time.sleep(5)
    countDownElement = c.find_element_by_class_name('main-curr-bonus-countdown')
    if any(char.isdigit() for char in countDownElement.text):
        countDownTime = int(countDownElement.text[0:countDownElement.text.index(' ')])
    else:
        countDownTime = 7680

    if countDownTime < 120:
        os.system(r'd:\curl\bin\curl -X POST --data "{\"method\":\"xdag_do_xfer\", \"params\":[{\"amount\":\"10\", \"address\":\"0vFAaFwfrh9vnwhXHm0zx3cDKqRJJtrR\", \"remark\":\"REMARK\"}], \"id\":1}" 127.0.0.1:8888')
        time.sleep(120)

    time.sleep(60)