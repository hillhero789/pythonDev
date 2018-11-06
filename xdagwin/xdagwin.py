#!/usr/bin/python
# # -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup  
import re
import gc

txs = []
txs1 = []
pageAddr = 'https://explorer.xdag.io/block/SNiOG7aUUyZ3QmSl87T0CsUezb5C5l5X'
explorerAddr =  'https://explorer.xdag.io/block/'

def getAllTxs(paraTxs, href):#获取某个地址所有交易，paraTxs为外部传入字符串list用于返回计算结果
        res = requests.get(href)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        tds = soup.tbody.find_all('td')

        for i in range(0, len(tds) - 2):
                paraTxs.append(tds[i].get_text().strip())
        
        newHref = soup.find(string = "Next")
        if 'https' in newHref.parent['href']:
                getAllTxs(paraTxs, newHref.parent['href'])

def getRecentTx(paraTxs, href):#获取某个地址最近一笔交易
        res = requests.get(href)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        tds = soup.tbody.find_all('td')
        for i in range(0, 4):
                paraTxs.append(tds[i].get_text().strip())

def getWalletAddr(direction, txHash):
        res = requests.get(explorerAddr + txHash)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        tds = soup.tbody.find_all('td')
        if direction == 'input':
                return tds[4].get_text().strip()
        else:
                return tds[10].get_text().strip()

getAllTxs(txs, pageAddr) 
getRecentTx(txs1,pageAddr)
print(txs1[1] == txs[1])        #证明获取所有交易期间没有增加新的交易
print(getWalletAddr('output',txs[1]))
print(getWalletAddr('input',txs[13]))







#aaa = soup.find(string = "Next")#("a", class_ = re.compile("secondary small") )
#print(tds[0].get_text().strip())
#for item in aaa:
#print(aaa.parent['href'])
