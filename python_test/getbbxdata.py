#!/usr/bin/python
# # -*- coding: utf-8 -*-
from selenium import webdriver
c = webdriver.Chrome()
c.get('https://www.bbx.com/exchange?coinPair=XDAG/ETH')
comment = c.find_element_by_class_name('dynamic-data')
#count = comment.find_element_by_class_name('f_red')
print(comment.text)
c.close()