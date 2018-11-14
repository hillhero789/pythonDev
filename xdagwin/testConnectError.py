#!/usr/bin/python
# # -*- coding: utf-8 -*-

import requests
while True:
    try:
        res = requests.get('https://explorer.xdag.io/block/SNiOG7aUUyZ3QmSl87T0CsUezb5C5l5X')
    except requests.exceptions.ConnectionError:
        next

