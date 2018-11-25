#!/usr/bin/python
# # -*- coding: utf-8 -*-
import requests
import json
import time
import datetime
import sys
import gc

allInputTxs = []                    #[wallet，哈希，数量，时间，...]
allOutputTxs = []                   #[wallet，哈希，数量，时间，...]
    # The RPC server url
txsLatestDict = {'Input': '', 'Output': ''}

def getXdagRpcJson(url, body, attemptTimes = 10):
        errorCounter = 0
        connError = 0
        while True:
                try:
                        resp = requests.post(url, data = json.dumps(body))
                        print(str(datetime.datetime.now())+' after requests post')
                        resultJson = resp.json()
                        if 'error' not in resultJson.keys():
                                break
                        else:
                                errorCounter += 1
                                print(str(datetime.datetime.now()) +' get data error for '+ str(errorCounter) +' times!')
                                if errorCounter >= attemptTimes:
                                        print(str(datetime.datetime.now()) +' get data ERROR!')
                                        return None
                                time.sleep(10)
                                continue
                except requests.exceptions.ConnectionError:
                        connError += 1
                        print(str(datetime.datetime.now()) +' Connection error for '+ str(connError) +' times!')
                        time.sleep(3)
                        if connError >= attemptTimes:
                                print(str(datetime.datetime.now()) +' conn ERROR!')
                                return None
        return resultJson

def getAllTxs(paraInputTxs, paraOutputTxs, walletAddr):
    url = 'http://pool.xdag.us:7667'
    body = {"method":"xdag_get_transactions", "params":[{"address":walletAddr, "page":0, "pagesize":1000}], "id":1}
    resultJson = getXdagRpcJson(url, body)

    if resultJson is not None:
        for r in resultJson['result']['transactions']:
            if r['state'] =='Accepted':
                body = {"method":"xdag_get_block_info", "params":[r['address']], "id":1}
                resultJson1 = getXdagRpcJson(url, body)
                if resultJson1 is not None:
                    if r['direction'] == 'input':
                        paraInputTxs.append(resultJson1['result'][0]['transactions'][2]['address'])
                        paraInputTxs.append(r['address'])
                        paraInputTxs.append(r['amount'])
                        paraInputTxs.append(r['timestamp'])
                    else:
                        paraOutputTxs.append(resultJson1['result'][0]['transactions'][3]['address'])
                        paraOutputTxs.append(r['address'])
                        paraOutputTxs.append(r['amount'])
                        paraOutputTxs.append(r['timestamp'])

def getLatestTx(paraTxsDict, walletAddr):#获取最近一笔Input 和 Output 的哈希
    hasGetInput = False
    hasGetOutput = False
    url = 'http://pool.xdag.us:7667'
    body = {"method":"xdag_get_transactions", "params":[{"address":walletAddr, "page":0, "pagesize":1000}], "id":1}
    resultJson = getXdagRpcJson(url, body)
    if resultJson is not None:
        for r in resultJson['result']['transactions']:
            if r['state'] =='Accepted':
                if not hasGetInput and r['direction'] == 'input':
                    paraTxsDict['Input'] = r['address']
                    hasGetInput = True
                elif not hasGetOutput and r['direction'] == 'output':
                    paraTxsDict['Output'] = r['address']
                    hasGetOutput = True
                elif hasGetInput and hasGetOutput:
                    break

def getWalletAddr(txHash, direction):
    url = 'http://pool.xdag.us:7667'
    body = {"method":"xdag_get_block_info", "params":[txHash], "id":1}
    resultJson = getXdagRpcJson(url, body)
    if direction == 'input':
        return resultJson['result'][0]['transactions'][2]['address']
    else:
        return resultJson['result'][0]['transactions'][3]['address']



def doXfer(walletAddr, ammount):#向胜利者发送XDAG       成功返回交易哈希，失败返回None
        url = 'http://127.0.0.1:8888'
        body = {"method":"xdag_do_xfer", "params":[{"amount":str('%.9f'%(ammount)), "address":walletAddr, "remark":"REMARK"}], "id":1}
        resultJson = getXdagRpcJson(url, body)
        
        if resultJson is not None:
            return resultJson['result'][0]['block']
        else:
            return None


url = 'http://pool.xdag.us:7667'
body = {"method":"xdag_get_transactions", "params":[{"address":"ovjaYrrxw/IuK7UHAWv5d9ByWCdQPTrS", "page":0, "pagesize":20}], "id":1}
resultJson = getXdagRpcJson(url, body)
print(sys.getsizeof(resultJson))
del(resultJson)
print(gc.collect())



