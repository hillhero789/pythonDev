#!/usr/bin/python
# # -*- coding: utf-8 -*-
import requests
import json
import time
import datetime
import sys
import gc
#TB transaction block
#   FJoUrVoHgsbMKHH8JLlEz53tQ6KoYsmr Main block --> 1BImy6+8pitSdWNZlEilnL+FMTZeXMYi
#   NEPcQ849G2ADsWCx2m6ZjkfY8FwBSs30            TB: 1BImy6+8pitSdWNZlEilnL+FMTZeXMYi :  NNHWNzjXq0CB7wo4atu4DuW+RTNnwv+Y  0.1 to NEPcQ849G2ADsWCx2m6ZjkfY8FwBSs30
#                                               TB: /69sInEMhLekXm9a0nfYa8+jsSDQlsgA
#   NNHWNzjXq0CB7wo4atu4DuW+RTNnwv+Y

url = 'http://207.148.112.122:7667'
#body = {"method":"xdag_get_balance", "params":["pRRhtN/MqUlS141CbX7L2sWNoR7e3LTA"], "id":1}        #balance
#body = {"method":"xdag_do_xfer", "params":[{"amount":"0.2", "address":"NEPcQ849G2ADsWCx2m6ZjkfY8FwBSs30", "remark":"test"}], "id":1}       #xfer
body = {"method":"xdag_get_block_info", "params":["7LjfZ3Cm8bAev14VkO/P9N5xW4du3AJj"], "id":1}      #get block
#body = {"method":"xdag_get_transactions", "params":[{"address":"pRRhtN/MqUlS141CbX7L2sWNoR7e3LTA", "page":0, "pagesize":50}], "id":1}

resp = requests.post(url, data = json.dumps(body))
resultJson = resp.json()
print(resp.text)