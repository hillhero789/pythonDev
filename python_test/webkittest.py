#!/usr/bin/python
# # -*- coding: utf-8 -*-
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
c = webdriver.Chrome()
c.get('http://vbitex.com/Home/Qcorders/index/currency/XDAG.html')

while True:
    try:
        comment = c.find_element_by_id('from_over')
        break
    except NoSuchElementException:
        print('NO SUCH!')
        time.sleep(30)
        #raise
print(comment.text)