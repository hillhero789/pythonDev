#!/usr/bin/python
# # -*- coding: utf-8 -*-
import requests
import json
import time
import datetime
import sys
import gc

a = {
    "time":"2018-07-11 16:38:24.504",
    "timestamp":"16d18ca0205",
    "flags":"1c",
    "state":"Accepted",
    "file_pos":"e00",
    "hash":"4ee22e5da5b979140ba1eb3058add7faff1d75c757b6b38a3d0887b7ba4e2604",
    "difficulty":"6a5a22b4abf81b1ec9679b64dce",
    "balance_address":"BCZOureHCD2Ks7ZXx3Ud//rXrVgw66EL",
    "balance":"0.000000000",
    "block_as_transaction":[
        {
            "direction":"fee",
            "address":"GejHxhxx5VieyGu2nc3eVH9UUIHWVJkE",
            "amount":"0.000000000"
        },
        {
            "direction":"input",
            "address":"ww3E6ITb8cU96n3dQ1C8GidxkZOWPIyO",
            "amount":"243.493238782"
        }
    ],
    "block_as_address":[],
    "total_fee":0.000000000,
    "total_inputs":243.493238782,
    "total_outputs":243.493238777,
    "kind":"Transaction block"
}

b = {
    "time":"2018-06-27 19:27:59.999",
    "timestamp":"16ccf94ffff",
    "flags":"1f",
    "state":"Main",
    "file_pos":"19200",
    "hash":"0000000000001de7c93aaf99caf68f36a49895b20dab06b2e93a2c788659ea19",
    "difficulty":"684bc5abbf2e34ce9bd55442320",
    "balance_address":"GepZhngsOumyBqsNspWYpDaP9sqZrzrJ",
    "balance":"10.240000054",
    "block_as_transaction":[
        {
            "direction":"fee",
            "address":"GepZhngsOumyBqsNspWYpDaP9sqZrzrJ",
            "amount":"0.000000000"
        },
        {
            "direction":"output",
            "address":"dhy1Z5W3QSUHlLpEGaAUlqDWFZ/crCHm",
            "amount":"0.000000000"
        }
    ],
    "block_as_address":[
        {
            "direction":"earning",
            "address":"GepZhngsOumyBqsNspWYpDaP9sqZrzrJ",
            "amount":"1024.000000000",
            "time":"2018-06-27 19:27:59.999"
        },
        {
            "direction":"output",
            "address":"kT86tjhtGZLAhSzAelGD8Zyme9aF5/4T",
            "amount":"15.829778345",
            "time":"2018-06-27 19:42:56.738"
        }
    ],
    "balances_last_week":[
        {
            "2018-06-21":"0"
        },
        {
            "2018-06-22":"0"
        },
        {
            "2018-06-23":"0"
        },
        {
            "2018-06-24":"0"
        },
        {
            "2018-06-25":"0"
        },
        {
            "2018-06-26":"0"
        },
        {
            "2018-06-27":"1024.000000000"
        }
    ],
    "earnings_last_week":[
        {
            "2018-06-21":"0"
        },
        {
            "2018-06-22":"0"
        },
        {
            "2018-06-23":"0"
        },
        {
            "2018-06-24":"0"
        },
        {
            "2018-06-25":"0"
        },
        {
            "2018-06-26":"0"
        },
        {
            "2018-06-27":"1024.000000000"
        }
    ],
    "spendings_last_week":[
        {
            "2018-06-21":"0"
        },
        {
            "2018-06-22":"0"
        },
        {
            "2018-06-23":"0"
        },
        {
            "2018-06-24":"0"
        },
        {
            "2018-06-25":"0"
        },
        {
            "2018-06-26":"0"
        },
        {
            "2018-06-27":"1013.759999922"
        }
    ],
    "balance_change_last_24_hours":10.240000078,
    "earnings_change_last_24_hours":1024,
    "spendings_change_last_24_hours":1013.759999922,
    "total_earnings":1024.000000000,
    "total_spendings":1013.759999922,
    "kind":"Main block"
}

print(b['block_as_address'][0])

url = r'https://explorer.xdag.io/api/block/zEHEOBggVqqAhQ4XQWTIIGFI4tmysxJF'
resp = requests.get(url)
resultJson = resp.json()
print(resultJson['block_as_address']['address'])