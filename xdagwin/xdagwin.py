#!/usr/bin/python
# # -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup  
import os
import time
import json
import htmlCodes

makerFee = 0.00
takerFee = 0.05
fee = 0.0
stakeAmount = [10.0,100.99]
filepath = r'/var/www/html/index.html'
#以上参数需要提前设置

unmatchBet = []         #[传输哈希，数量，...]
matchBet = []           #[wallet, 传输哈希，数量，winner or loser，...]
newMatchBet = []        
allInputTxs = []        #[direction，哈希，数量，时间，...]
allOutputTxs = []       #[wallet，哈希，数量，时间，...]
newAllInputTxs = []     #获取最新输入交易
newAllOutputTxs = []    #获取最新输出交易
txsLatestDict = {'Input': '', 'Output': ''}        
pageAddr = 'https://explorer.xdag.io/block/dvNo7wYcVz4zl6qRUy+twdFZv7vIJiuW'
explorerAddr =  'https://explorer.xdag.io/block/'

def getPageData(href,tryTimes = 2):#增加错误处理，连接错误时可尝试多次，最终失败则返回空字符串
        i = 0
        res = None
        for i in range(0, tryTimes):
                try:
                        res = requests.get(href)
                        break
                except requests.exceptions.ConnectionError:
                        print('Get ' + href + ' data error for ' + str(i+1) + ' time.')
                        res = None
        return res

def getAllTxs(paraInputTxs, paraOutputTxs, href):#获取某个地址所有交易direction 为Input 或 Output，paraTxs为外部传入字符串list用于返回计算结果
        res = getPageData(href)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        tds = soup.tbody.find_all('td')
        if tds is not None:
                for i in range(0, len(tds) - 2,4):
                        if tds[i].get_text().strip() == 'Input': 
                                paraInputTxs.append(tds[i].get_text().strip())
                                paraInputTxs.append(tds[i+1].get_text().strip())
                                paraInputTxs.append(tds[i+2].get_text().strip())
                                paraInputTxs.append(tds[i+3].get_text().strip())
                        elif tds[i].get_text().strip() == 'Output':
                                paraOutputTxs.append(tds[i].get_text().strip())
                                paraOutputTxs.append(tds[i+1].get_text().strip())
                                paraOutputTxs.append(tds[i+2].get_text().strip())
                                paraOutputTxs.append(tds[i+3].get_text().strip())
                        
        newHref = soup.find(text = "Next")
        if newHref is not None:
                if 'https' in newHref.parent['href']:
                        getAllTxs(paraInputTxs, paraOutputTxs, newHref.parent['href'])

def getLatestTx(paraTxsDict, href):#获取最近一笔Input 和 Output 的哈希
        hasGetInput = False
        hasGetOutput = False
        res = getPageData(href)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        tds = soup.tbody.find_all('td')
        if tds is not None:
                for i in range(0, len(tds) - 2,4):
                        if tds[i].get_text().strip() == 'Input' and not hasGetInput: 
                                paraTxsDict['Input'] = tds[i+1].get_text().strip()
                                hasGetInput = True
                        elif tds[i].get_text().strip() == 'Output' and not hasGetOutput:
                                paraTxsDict['Output'] = tds[i+1].get_text().strip()
                                hasGetOutput = True
                        elif hasGetInput and hasGetOutput:
                                break

def getWalletAddr(direction, txHash):#根据传输哈希获取对应的钱包地址，direction 表示交易传输方向
        res = getPageData(explorerAddr + txHash)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        tds = soup.tbody.find_all('td')
        if tds is not None:
                if direction == 'Input':
                        return tds[4].get_text().strip()
                else:
                        return tds[10].get_text().strip()
        else:
                return None

def getMatchAndUnmatchBet(paraInputTxs, paraMatchBet, paraUnmatchBet):#paraInputTxs为输入交易列表
        tmpHash = ''
        tmpStr = 'loser'
        i = len(paraInputTxs) - 3        # i 是传输哈希，i+1 是数量   计算出已经完成的bet，和未完成的bet
        while i >0:
                try:
                        j = paraUnmatchBet.index(paraInputTxs[i+1])
                except ValueError:
                        j = -1

                if j == -1 :
                        paraUnmatchBet.append(paraInputTxs[i])
                        paraUnmatchBet.append(paraInputTxs[i+1])
                else:
                        tmpHash = paraUnmatchBet.pop(j-1)       #将原来在不匹配列表中的数据加入到匹配列表
                        paraMatchBet.append('')                 #钱包地址暂时为空
                        paraMatchBet.append(tmpHash)
                        paraMatchBet.append(paraUnmatchBet.pop(j-1))
                        if calTxVal(tmpHash) < calTxVal(paraInputTxs[i]):
                                paraMatchBet.append('loser')
                                tmpStr = 'winner'
                        else:
                                paraMatchBet.append('winner')
                                tmpStr = 'loser'

                        paraMatchBet.append('')                 #将inputTxs中的数据加入到匹配列表，钱包地址暂时为空
                        paraMatchBet.append(paraInputTxs[i])
                        paraMatchBet.append(paraInputTxs[i+1])
                        paraMatchBet.append(tmpStr)
                i -= 4

def reward(paraOutputTxs, paraMatchBet):#获取所有output交易，判断是否已转入到matchBet对应的地址，如果是，则已完成，否则未完成，进行转账
        if paraMatchBet == []:
                return
        tmpWalletAddr = ''
        i = 0
        j = 0
        k = 0
        
        for j in range(0, len(paraOutputTxs), 4): #把输出交易表中的交易哈希转化为钱包地址
                paraOutputTxs[j] = getWalletAddr('Output', paraOutputTxs[j+1])   #把钱包地址填入outputTxs
        tmpOutputTxs = paraOutputTxs.copy()

        for i in range(0, len(paraMatchBet), 4):
                tmpWalletAddr = getWalletAddr('Input', paraMatchBet[i+1])
                paraMatchBet[i] = tmpWalletAddr                 #将matchBet中的钱包地址填入
                if paraMatchBet[i+3] == 'winner':
                        try:
                                #tmpWalletAddr = getWalletAddr('Input', paraMatchBet[i+1])
                                #paraMatchBet[i] = tmpWalletAddr                 
                                k = tmpOutputTxs.index(tmpWalletAddr)
                                while True:
                                        if float(tmpOutputTxs[k+2]) == float(paraMatchBet[i+2])*2.0*(1-fee):#找到钱包地址一致，且数量一致，则证明已完成
                                                tmpOutputTxs.pop(k-1)             #防止一个钱包相同金额赢了多次，不给转账
                                                tmpOutputTxs.pop(k-1)
                                                tmpOutputTxs.pop(k-1)
                                                tmpOutputTxs.pop(k-1)
                                                break
                                        else:
                                                k = tmpOutputTxs.index(tmpWalletAddr, k+1)#如果钱包地址一致，金额不一致，则继续向后查找，找不到了，则转账        
                        except ValueError:
                                doXfer(tmpWalletAddr, float(paraMatchBet[i+2])*2*(1-fee))

        #del(paraMatchBet[:])       #清空matchBet列表

                                

#需注意防止一个钱包赢了后多次向其转账，因为区块浏览器会有延迟，转账后没有那么快到账。
#可以通过返回的哈希值，再查询区块浏览器是否已经完成来确认
def doXfer(walletAddr, ammount):#向胜利者发送XDAG       成功返回交易哈希，失败返回None
        #print('xfer ' + float(ammount)*1.975 +' to ' + walletAddr)#for test
        #resultStr = os.system
        resultStr = os.popen(r'curl -X POST --data "{\"method\":\"xdag_do_xfer\", \"params\":[{\"amount\":\"' + str('%.9f'%(ammount)) + r'\", \"address\":\"' + walletAddr + r'\", \"remark\":\"REMARK\"}], \"id\":1}" 127.0.0.1:8888').read()

        if resultStr.find("result") == -1:
                print("\nxfer failed: Need to transfer " + str(ammount) + " to " + walletAddr)
                return None
        else:
                resultDict = json.loads(resultStr)
                return resultDict['result'][0]['block']

def calTxVal(paraTxHash):#计算传输哈希值
        s = 0 
        for char in paraTxHash:
                if char.isdigit():
                        s += int(char)
        return s

#############待实现################
def getNewInputTxs(topTxHash):#获取当前最新传输哈希值以后新交易，该函数目前仍存在异常！！！！分页时也不好实现
        res = getPageData(pageAddr)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,"html.parser")
        lastTx = soup.find('a',text = topTxHash)
        for newTx in lastTx.parent.previous_siblings:   #此方法无法获取之前的哈希值
                print(newTx)

def refreshPage(paraUnmatchBet, paraMatchBet):
        unmatchBetTableBody = ''
        matchBetTalbeBody = ''
        
        for i in range(0,len(paraUnmatchBet),2):
                unmatchBetTableBody = unmatchBetTableBody + r'<tr><td>' +paraUnmatchBet[i] + r'</td><td>' + str(calTxVal(paraUnmatchBet[i])) + r'</td><td>' + paraUnmatchBet[i+1] + r'</td></tr>'

        for i in range(len(paraMatchBet)-4, max(0,len(paraMatchBet)-44),-4):
                matchBetTalbeBody = matchBetTalbeBody + r'<tr><td>' + paraMatchBet[i] + r'</td><td>' + paraMatchBet[i+1] + r'</td><td>' + str(calTxVal(paraMatchBet[i+1])) + r'</td><td>' + paraMatchBet[i+2] + r'</td><td>' + paraMatchBet[i+3] + r'</td></tr>'

        f = open(filepath,'w+')
        f.write(htmlCodes.header)
        f.write(unmatchBetTableBody)
        f.write(htmlCodes.tableFooter)
        f.write(htmlCodes.tableHeader)
        f.write(matchBetTalbeBody)
        f.write(htmlCodes.footer)
        f.close()

#以下代码用于确认当前区块浏览器中记录的游戏已经清空
while True:     #获取所有交易数据
        getAllTxs(allInputTxs, allOutputTxs, pageAddr) 
        getLatestTx(txsLatestDict,pageAddr)
        if allInputTxs == []:   #空表示无交易，继续等待
                continue
        if txsLatestDict['Input'] == allInputTxs[1] and (allOutputTxs == [] or txsLatestDict['Output'] == allOutputTxs[1]):      #证明获取所有交易期间没有增加新的交易，如果不符合，则需重新获取所有交易
                break


getMatchAndUnmatchBet(allInputTxs,matchBet,unmatchBet)      #将匹配与未匹配交易进行记录
reward(allOutputTxs,matchBet)
refreshPage(unmatchBet, matchBet)



oldInputTxTopIndex = 1
oldInputTxTopHash = allInputTxs[1]

while True:
        while True:
                del(newAllInputTxs[:])  #清空
                del(newAllOutputTxs[:]) #清空
                getAllTxs(newAllInputTxs, newAllOutputTxs, pageAddr)
                getLatestTx(txsLatestDict, pageAddr)
                if newAllInputTxs == []:   #空表示无交易，继续等待
                        continue
                if txsLatestDict['Input'] == newAllInputTxs[1] and (newAllOutputTxs == [] or txsLatestDict['Output'] == newAllOutputTxs[1]):   #证明获取所有交易期间没有增加新的交易，如果不符合，则需重新获取所有交易
                        break

        oldInputTxTopIndex = newAllInputTxs.index(oldInputTxTopHash)
        if oldInputTxTopIndex == 1:
                continue
        else:
                getMatchAndUnmatchBet(newAllInputTxs[ 0 : oldInputTxTopIndex - 1], newMatchBet, unmatchBet)      #将新增交易记录到匹配与未匹配交易列表，得到新的匹配列表
                reward([], newMatchBet)                 #由于新的匹配交易，不可能有已经被支付过，所以reward第一个参数为空
                for newMatchBetItem in newMatchBet:     #向matchBet列表增加新元素，但是只保留最近30个，新元素在后，老元素在前
                        matchBet.append(newMatchBetItem)
                del(newMatchBet[:])
                if len(matchBet)>40:
                        del(matchBet[0:len(matchBet)-40])
                refreshPage(unmatchBet, makerFee)
        oldInputTxTopHash = newAllInputTxs[1]
        #time.sleep(10)