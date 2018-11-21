#!/usr/bin/python
# # -*- coding: utf-8 -*-
import requests
import json

#url = 'http://pool.xdag.us:7667' # The RPC server url
#body = {"method":"xdag_state", "params":[], "id":1}

url = 'http://127.0.0.1:8888'
body = {"method":"xdag_do_xfer", "params":[{"amount":"0.0000642", "address":"dvNo7wYcVz4zl6qRUy+twdFZv7vIJiuW", "remark":"REMARK"}], "id":1}
resp = requests.post(url, data = json.dumps(body))
print(resp.text)