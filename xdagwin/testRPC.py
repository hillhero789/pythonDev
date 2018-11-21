#!/usr/bin/python
# # -*- coding: utf-8 -*-
import requests
import json

#url = 'http://pool.xdag.us:7667' # The RPC server url
#body = {"method":"xdag_state", "params":[], "id":1}

url = 'http://127.0.0.1:8888'
body = {"method":"xdag_version", "params":[], "id":1}
resp = requests.post(url, data = json.dumps(body))
print(resp.text)