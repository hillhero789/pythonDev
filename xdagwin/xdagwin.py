#!/usr/bin/python
# # -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup  
import gc
import re

makerFee = 0.00
takerFee = 0.05
stakeAmount = [10.0,100.99]
#以上参数需要提前设置

unFinishedBet = []      #元素0为传输哈希，元素1为数量
hasFinishedBet = []     
txs = []
txs1 = []
pageAddr = 'https://explorer.xdag.io/block/SNiOG7aUUyZ3QmSl87T0CsUezb5C5l5X'
explorerAddr =  'https://explorer.xdag.io/block/'

def getAllInputTxs(paraTxs, href):#获取某个地址所有交易，paraTxs为外部传入字符串list用于返回计算结果
        res = requests.get(href)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        tds = soup.tbody.find_all('td')
        for i in range(0, len(tds) - 2,4):
                if tds[i].get_text().strip() == "Input": 
                        paraTxs.append(tds[i].get_text().strip())
                        paraTxs.append(tds[i+1].get_text().strip())
                        paraTxs.append(tds[i+2].get_text().strip())
                        paraTxs.append(tds[i+3].get_text().strip())
        
        newHref = soup.find(text = "Next")
        if 'https' in newHref.parent['href']:
                getAllInputTxs(paraTxs, newHref.parent['href'])

def getRecentInputTx(paraTxs, href):#获取某个地址最近一笔交易
        res = requests.get(href)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        tds = soup.tbody.find_all('td')
        for i in range(0, len(tds) - 2,4):
                if tds[i].get_text().strip() == "Input": 
                        paraTxs.append(tds[i].get_text().strip())
                        paraTxs.append(tds[i+1].get_text().strip())
                        paraTxs.append(tds[i+2].get_text().strip())
                        paraTxs.append(tds[i+3].get_text().strip())
                        break

def getInputWalletAddr(txHash):#根据传输哈希获取对应的钱包地址，direction 表示交易传输方向
        res = requests.get(explorerAddr + txHash)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        tds = soup.tbody.find_all('td')
        return tds[4].get_text().strip()

def getNewInputTxs(topTxHash):#获取当前最新传输哈希值以后新交易
        res = requests.get(pageAddr)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        lastTx = soup.find('a',text = topTxHash)
        for newTx in lastTx.parent.previous_siblings:
                print(newTx)

def doXfer():

        return None




while True:
        getAllInputTxs(txs, pageAddr) 
        getRecentInputTx(txs1,pageAddr)
        if txs1[1] == txs[1]:                   #证明获取所有交易期间没有增加新的交易，如果不符合，则需重新获取所有交易
                break

getNewInputTxs('\n\t\t\t\t\t\t\t'+txs[9]+'\n\t\t\t\t\t\t')


'''
i = len(txs) - 3
while i >0:# i 是传输哈希，i+1 是数量   计算出已经完成的bet，和未完成的bet
        try:
                j = unFinishedBet.index(txs[i+1])
        except ValueError:
                j = -1

        if j == -1 :
                unFinishedBet.append(txs[i])
                unFinishedBet.append(txs[i+1])
        else:
                hasFinishedBet.append(unFinishedBet.pop(j-1))
                hasFinishedBet.append(unFinishedBet.pop(j-1))
                hasFinishedBet.append(txs[i])
                hasFinishedBet.append(txs[i+1])
        i -=4
        
print(len(unFinishedBet))
print(len(hasFinishedBet))
print(len(txs))
'''
