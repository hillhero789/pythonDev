#!/usr/bin/python
# # -*- coding: utf-8 -*-
import json
import time
import requests
import datetime

def getXdagRpcJson(url, body, attemptTimes = 10):
    errorCounter = 0
    connError = 0
    while True:
        try:
            resp = requests.post(url, data = json.dumps(body))
            resultJson = resp.json()
            if 'error' not in resultJson.keys():
                break
            else:
                errorCounter += 1
                print(str(datetime.datetime.now()) +' get data error for '+ str(errorCounter) +' times!')
                if errorCounter >= attemptTimes:
                    print(str(datetime.datetime.now()) +' get data ERROR!')
                    return None
                time.sleep(3)
                continue
        except requests.exceptions.ConnectionError:
            connError += 1
            print(str(datetime.datetime.now()) +' Connection error for '+ str(connError) +' times!')
            time.sleep(3)
            if connError >= attemptTimes:
                print(str(datetime.datetime.now()) +' conn ERROR!')
                return None
    return resultJson

def checkXdagState():
    url = 'http://127.0.0.1:8888'
    body = {"method":"xdag_state", "params":[], "id":1}
    resultJson = getXdagRpcJson(url, body)
    print(resultJson['result'][0])

def restartXDAG():
    return None

while True:
    checkXdagState()
    time.sleep(60)