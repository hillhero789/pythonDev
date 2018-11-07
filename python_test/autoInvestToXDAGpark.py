#!/usr/bin/python
# # -*- coding: utf-8 -*-
from selenium import webdriver
import time
import datetime
import os
c = webdriver.Firefox()
lastRound = 0
isfirst = True
countDownTime = 0
while True:
    c.get('http://fomoxdag.xdagpark.com/')
    time.sleep(10)
    
    comment = c.find_elements_by_class_name('color-pink')
    if isfirst:
        lastRound = int(comment[1].text)
        isfirst = False
        
    countDownElement = c.find_element_by_class_name('main-curr-bonus-countdown')
    if any(char.isdigit() for char in countDownElement.text):
        countDownTime = int(countDownElement.text[0:countDownElement.text.index(' ')])
    
    if countDownTime > 300:
        time.sleep(countDownTime-300)

    if int(comment[1].text) > lastRound:
        print(comment[1].text + r' ' + str(datetime.datetime.now()))
        lastRound = int(comment[1].text)
        os.system(r'd:\curl\bin\curl -X POST --data "{\"method\":\"xdag_do_xfer\", \"params\":[{\"amount\":\"10\", \"address\":\"0vFAaFwfrh9vnwhXHm0zx3cDKqRJJtrR\", \"remark\":\"REMARK\"}], \"id\":1}" 127.0.0.1:8888')
    

