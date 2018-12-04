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

url = 'http://106.12.130.174:7667'
#body = {"method":"xdag_get_balance", "params":["NEPcQ849G2ADsWCx2m6ZjkfY8FwBSs30"], "id":1}        #balance
#body = {"method":"xdag_do_xfer", "params":[{"amount":"0.2", "address":"NEPcQ849G2ADsWCx2m6ZjkfY8FwBSs30", "remark":"test"}], "id":1}       #xfer
body = {"method":"xdag_get_block_info", "params":["GcUUbfT1vvD5Aw1hTZupfZu7JxtyoMoP"], "id":1}      #get block
#body = {"method":"xdag_get_transactions", "params":[{"address":"NEPcQ849G2ADsWCx2m6ZjkfY8FwBSs30", "page":0, "pagesize":50}], "id":1}

resp = requests.post(url, data = json.dumps(body))
resultJson = resp.json()
print(resp.text)