#!/usr/bin/python
# # -*- coding: utf-8 -*-
import requests
import json
import time
import datetime
import sys
import gc

url = r'https://explorer.xdag.io/api/block/zEHEOBggVqqAhQ4XQWTIIGFI4tmysxJF'
resp = requests.get(url)
resultJson = resp.json()
print(resultJson['block_as_address']['address'])