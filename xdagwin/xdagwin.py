#!/usr/bin/python
# # -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup  
import gc
import re
import time

makerFee = 0.00
takerFee = 0.05
stakeAmount = [10.0,100.99]
#以上参数需要提前设置

unmatchBet = []      #元素0为传输哈希，元素1为数量
matchBet = []     
allInputTxs = []
newAllInputTxs = []
txsLatest = []
pageAddr = 'https://explorer.xdag.io/block/SNiOG7aUUyZ3QmSl87T0CsUezb5C5l5X'
explorerAddr =  'https://explorer.xdag.io/block/'

def getAllTxs(direction, paraTxs, href):#获取某个地址所有交易direction 为Input 或 Output，paraTxs为外部传入字符串list用于返回计算结果
        res = requests.get(href)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        tds = soup.tbody.find_all('td')
        for i in range(0, len(tds) - 2,4):
                if tds[i].get_text().strip() == direction: 
                        paraTxs.append(tds[i].get_text().strip())
                        paraTxs.append(tds[i+1].get_text().strip())
                        paraTxs.append(tds[i+2].get_text().strip())
                        paraTxs.append(tds[i+3].get_text().strip())
        
        newHref = soup.find(text = "Next")
        if 'https' in newHref.parent['href']:
                getAllTxs(direction, paraTxs, newHref.parent['href'])

def getRecentTx(direction, paraTxs, href):#获取某个地址最近一笔交易
        res = requests.get(href)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        tds = soup.tbody.find_all('td')
        for i in range(0, len(tds) - 2,4):
                if tds[i].get_text().strip() == direction: 
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

def getMatchAndUnmatchBet(paraTxs):
        tmpHash = ''
        tmpStr = 'loser'
        i = len(paraTxs) - 3        # i 是传输哈希，i+1 是数量   计算出已经完成的bet，和未完成的bet
        while i >0:
                try:
                        j = unmatchBet.index(paraTxs[i+1])
                except ValueError:
                        j = -1

                if j == -1 :
                        unmatchBet.append(paraTxs[i])
                        unmatchBet.append(paraTxs[i+1])
                else:
                        tmpHash = unmatchBet.pop(j-1)
                        matchBet.append(tmpHash)
                        matchBet.append(unmatchBet.pop(j-1))
                        if calTxVal(tmpHash) < calTxVal(paraTxs[i]):
                                matchBet.append('loser')
                                tmpStr = 'winner'
                        else:
                                matchBet.append('winner')
                                tmpStr = 'loser'
                        matchBet.append(paraTxs[i])
                        matchBet.append(paraTxs[i+1])
                        matchBet.append(tmpStr)
                i -= 4

def checkIfFinished(paraMatchBet):#获取所有output交易，判断是否是转入到matchBet对应的地址，如果是，则已完成，否则未完成，进行转账
        
        return None

def doXfer(walletAddr):#向胜利者发送XDAG

        return None

def calTxVal(paraTxHash):#计算传输哈希值
        s = 0 
        for char in paraTxHash:
                if char.isdigit():
                        s += int(char)
        return s



while True:     #获取所有交易数据
        getAllTxs('Input', allInputTxs, pageAddr) 
        getRecentTx('Input',txsLatest,pageAddr)
        if txsLatest[1] == allInputTxs[1]:      #证明获取所有交易期间没有增加新的交易，如果不符合，则需重新获取所有交易
                break


getMatchAndUnmatchBet(allInputTxs)      #将匹配与不匹配交易进行记录


time.sleep(60)

while True:
        getAllTxs('Input', newAllInputTxs, pageAddr) 
        getRecentTx('Input',txsLatest,pageAddr)
        if txsLatest[1] == newAllInputTxs[1]:   #证明获取所有交易期间没有增加新的交易，如果不符合，则需重新获取所有交易
                break







###############
if newAllInputTxs[1] == allInputTxs[1]:
        time.sleep(60)
else:
        try:
                ptr = newAllInputTxs.index(allInputTxs[1])
        except ValueError:
                ptr = 1 
        if ptr != 1:
                for i in range(ptr-4, 0, -4):
                        unmatchBet.append(newAllInputTxs[i])
                        unmatchBet.append(newAllInputTxs[i+1])

#getNewInputTxs('\n\t\t\t\t\t\t\t' + allInputTxs[9] + '\n\t\t\t\t\t\t')





