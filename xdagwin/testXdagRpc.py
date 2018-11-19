#!/usr/bin/python
# # -*- coding: utf-8 -*-
import requests
import json

url = 'http://127.0.0.1:8888' # The RPC server url
body = {"method":"xdag_state", "params":[], "id":1}
print(body)
resp = requests.post(url, data = json.dumps(body))
print(resp.text)