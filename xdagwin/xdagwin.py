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

unmatchBet = []         #[传输哈希，数量，...]
matchBet = []           #[传输哈希，数量，winner or loser，...]
allInputTxs = []        #[direction，哈希，数量，时间，...]
allOutputTxs = []       #[direction，哈希，数量，时间，...]
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

def getLatestTx(direction, paraTxs, href):#获取某个地址最近一笔交易
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

def getWalletAddr(direction, txHash):#根据传输哈希获取对应的钱包地址，direction 表示交易传输方向
        res = requests.get(explorerAddr + txHash)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        tds = soup.tbody.find_all('td')
        if direction == 'Input':
                return tds[4].get_text().strip()
        else:
                return tds[10].get_text().strip()

def getNewInputTxs(topTxHash):#获取当前最新传输哈希值以后新交易
        res = requests.get(pageAddr)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        lastTx = soup.find('a',text = topTxHash)
        for newTx in lastTx.parent.previous_siblings:
                print(newTx)

def getMatchAndUnmatchBet(paraAllInputTxs,paraMatchBet, paraUnmatchBet):#paraAllInputTxs为所有输入交易列表
        tmpHash = ''
        tmpStr = 'loser'
        i = len(paraAllInputTxs) - 3        # i 是传输哈希，i+1 是数量   计算出已经完成的bet，和未完成的bet
        while i >0:
                try:
                        j = paraUnmatchBet.index(paraAllInputTxs[i+1])
                except ValueError:
                        j = -1

                if j == -1 :
                        paraUnmatchBet.append(paraAllInputTxs[i])
                        paraUnmatchBet.append(paraAllInputTxs[i+1])
                else:
                        tmpHash = paraUnmatchBet.pop(j-1)
                        paraMatchBet.append(tmpHash)
                        paraMatchBet.append(paraUnmatchBet.pop(j-1))
                        if calTxVal(tmpHash) < calTxVal(paraAllInputTxs[i]):
                                paraMatchBet.append('loser')
                                tmpStr = 'winner'
                        else:
                                paraMatchBet.append('winner')
                                tmpStr = 'loser'
                        paraMatchBet.append(paraAllInputTxs[i])
                        paraMatchBet.append(paraAllInputTxs[i+1])
                        paraMatchBet.append(tmpStr)
                i -= 4

def checkIfReward(paraOutputTxs, paraMatchBet):#获取所有output交易，判断是否是转入到matchBet对应的地址，如果是，则已完成，否则未完成，进行转账
        tmpWalletAddr = ''
        i = 0
        j = 0
        k = 0
        
        for j in range(0, len(paraOutputTxs)-4, 4): #把输出交易表中的交易哈希转化为钱包地址
                paraOutputTxs[j+1] = getWalletAddr('Output', paraOutputTxs[j+1])

        for i in range(0, len(paraMatchBet)-3, 3):
                if paraMatchBet[i+2] == 'winner':
                        try:
                                tmpWalletAddr = getWalletAddr('Input', paraMatchBet[i])
                                k = paraOutputTxs.index(tmpWalletAddr)
                                while True:
                                        if paraOutputTxs[k+1] == paraMatchBet[i+1]:#找到钱包地址一致，且数量一致，则证明已完成
                                                paraOutputTxs.pop(k-1)             #防止一个钱包相同金额赢了多次，不给转账
                                                paraOutputTxs.pop(k-1)
                                                paraOutputTxs.pop(k-1)
                                                paraOutputTxs.pop(k-1)
                                                break
                                        else:
                                                k = paraOutputTxs.index(tmpWalletAddr, k+1)#如果钱包地址一致，金额不一致，则继续向后查找，找不到了，则转账
                                                
                        except ValueError:
                                doXfer(tmpWalletAddr, paraMatchBet[i+1])


#需注意防止一个钱包赢了后多次向其转账，因为区块浏览器会有延迟，转账后没有那么快到账。
def doXfer(walletAddr, ammount):#向胜利者发送XDAG
        print('xfer ' + ammount +' to ' + walletAddr)#for test
        return None

def calTxVal(paraTxHash):#计算传输哈希值
        s = 0 
        for char in paraTxHash:
                if char.isdigit():
                        s += int(char)
        return s



while True:     #获取所有交易数据
        getAllTxs('Input', allInputTxs, pageAddr) 
        getLatestTx('Input',txsLatest,pageAddr)
        if txsLatest[1] == allInputTxs[1]:      #证明获取所有交易期间没有增加新的交易，如果不符合，则需重新获取所有交易
                break

txsLatest = []


while True:     #获取所有交易数据
        getAllTxs('Output', allOutputTxs, pageAddr) 
        getLatestTx('Output',txsLatest,pageAddr)
        if txsLatest[1] == allOutputTxs[1]:      #证明获取所有交易期间没有增加新的交易，如果不符合，则需重新获取所有交易
                break

getMatchAndUnmatchBet(allInputTxs,matchBet,unmatchBet)      #将匹配与未匹配交易进行记录
checkIfReward(allOutputTxs,matchBet)

time.sleep(60)

while True:
        getAllTxs('Input', newAllInputTxs, pageAddr) 
        getLatestTx('Input',txsLatest,pageAddr)
        if txsLatest[1] == newAllInputTxs[1]:   #证明获取所有交易期间没有增加新的交易，如果不符合，则需重新获取所有交易
                break







###############
'''
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

'''



