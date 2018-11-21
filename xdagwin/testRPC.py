#!/usr/bin/python
# # -*- coding: utf-8 -*-
import requests
import json

url = 'http://pool.xdag.us:7667' # The RPC server url
body = {"method":"xdag_get_transactions", "params":[{"address":"dvNo7wYcVz4zl6qRUy+twdFZv7vIJiuW", "page":2, "pagesize":10}], "id":1}

#url = 'http://127.0.0.1:8888'
#body = {"method":"xdag_do_xfer", "params":[{"amount":"0.0001284", "address":"7eZXBkNI4kVtVq8Y4eoO/I3OcIEulgWN", "remark":"REMARK"}], "id":1}
resp = requests.post(url, data = json.dumps(body))
a = resp.json
for j in a['result']['transactions']:
    print(j['address'])