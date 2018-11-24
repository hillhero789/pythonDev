#!/usr/bin/python
# # -*- coding: utf-8 -*-
import requests
import time
import json
import htmlCodes
import datetime
import gc

fee = 0.0
filepath = r'/var/www/html/index.html'
#以上参数需要提前设置

unmatchBet = []         #[wallet, 传输哈希，数量，...]
matchBet = []           #[wallet, 传输哈希，数量，winner or loser，...]
newMatchBet = []        
allInputTxs = []        #[wallet，哈希，数量，时间，...]
allOutputTxs = []       #[wallet，哈希，数量，时间，...]
newAllInputTxs = []     #获取最新输入交易
newAllOutputTxs = []    #获取最新输出交易
txsLatestDict = {'Input': '', 'Output': ''}        
WALLETADDR = 'ovjaYrrxw/IuK7UHAWv5d9ByWCdQPTrS'

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

def getWalletAddr(direction, txHash):#根据传输哈希获取对应的钱包地址，direction 表示交易传输方向
        print('In getWalletAddr')   #debug
        url = 'http://pool.xdag.us:7667'
        body = {"method":"xdag_get_block_info", "params":[txHash], "id":1}
        resultJson = getXdagRpcJson(url, body)
        if direction == 'input':
                return resultJson['result'][0]['transactions'][2]['address']
        else:
                return resultJson['result'][0]['transactions'][3]['address']
        print('leave getWalletAddr')   #debug

def getAllTxs(paraInputTxs, paraOutputTxs, walletAddr, pageSize=20 ):#获取对应钱包地址的所有输入、输出交易
        print('In getAllTxs')   #debug
        url = 'http://pool.xdag.us:7667'
        body = {"method":"xdag_get_transactions", "params":[{"address":walletAddr, "page":0, "pagesize":pageSize}], "id":1}
        resultJson = getXdagRpcJson(url, body)
        print('after getXdagRpcJson')   #debug
        if resultJson is not None:
                for r in resultJson['result']['transactions']:
                        if r['state'] =='Accepted':
                                if r['direction'] == 'input':
                                        paraInputTxs.append(getWalletAddr('input', r['address']))
                                        paraInputTxs.append(r['address'])
                                        paraInputTxs.append(r['amount'])
                                        paraInputTxs.append(r['timestamp'])
                                else:
                                        paraOutputTxs.append(getWalletAddr('output', r['address']))
                                        paraOutputTxs.append(r['address'])
                                        paraOutputTxs.append(r['amount'])
                                        paraOutputTxs.append(r['timestamp'])
        print('leave getAllTxs')  #debug
        return int(resultJson['result']['total'])

def getNewTxs(paraInputTxs, paraOutputTxs, walletAddr, pageSize=20 ):# 与getAllTxs区别在于先不填写钱包地址
        print('In getNewTxs')   #debug
        url = 'http://pool.xdag.us:7667'
        body = {"method":"xdag_get_transactions", "params":[{"address":walletAddr, "page":0, "pagesize":pageSize}], "id":1}
        resultJson = getXdagRpcJson(url, body)
        print('after getXdagRpcJson')   #debug
        if resultJson is not None:
                for r in resultJson['result']['transactions']:
                        if r['state'] =='Accepted':
                                if r['direction'] == 'input':
                                        paraInputTxs.append('')
                                        paraInputTxs.append(r['address'])
                                        paraInputTxs.append(r['amount'])
                                        paraInputTxs.append(r['timestamp'])
                                else:
                                        paraOutputTxs.append('')
                                        paraOutputTxs.append(r['address'])
                                        paraOutputTxs.append(r['amount'])
                                        paraOutputTxs.append(r['timestamp'])
        print('leave getNewTxs')  #debug

def getNewInputTxsWallet(paraInputTxs, endIndex):
        for i in range(0, endIndex, 4):
                paraInputTxs[i] = getWalletAddr('input', paraInputTxs[i+1])

def getLatestTx(paraTxsDict, walletAddr, pageSize=20):#获取最近一笔Input 和 Output 的哈希
        print('In getLatestTx')   #debug
        hasGetInput = False
        hasGetOutput = False
        url = 'http://pool.xdag.us:7667'
        body = {"method":"xdag_get_transactions", "params":[{"address":walletAddr, "page":0, "pagesize":pageSize}], "id":1}
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
        print('leave getLatestTx')  #debug

def getMatchAndUnmatchBet(paraInputTxs, paraMatchBet, paraUnmatchBet):#paraInputTxs为输入交易列表
        print('In getMatchAndUnmatchBet') #debug
        tmpHash = ''
        tmpWallet = ''
        tmpStr = 'loser'
        i = len(paraInputTxs) - 3        # i-1是钱包地址，i 是传输哈希，i+1 是数量   计算出已经完成的bet，和未完成的bet
        while i >0:
                try:
                        j = paraUnmatchBet.index(paraInputTxs[i+1]) #找到数量一致的位置
                except ValueError:
                        j = -1

                if j == -1 :#表示当前输入交易没有与不匹配列表中数量一致的项目
                        paraUnmatchBet.append(paraInputTxs[i-1])
                        paraUnmatchBet.append(paraInputTxs[i])
                        paraUnmatchBet.append(paraInputTxs[i+1])
                else:
                        tmpWallet = paraUnmatchBet.pop(j-2)     #将原来在不匹配列表中的数据加入到匹配列表
                        tmpHash = paraUnmatchBet.pop(j-2)     

                        paraMatchBet.append(tmpWallet)          
                        paraMatchBet.append(tmpHash)
                        paraMatchBet.append(paraUnmatchBet.pop(j-2))
                        if calTxVal(tmpHash) < calTxVal(paraInputTxs[i]):
                                paraMatchBet.append('loser')
                                tmpStr = 'winner'
                        else:
                                paraMatchBet.append('winner')
                                tmpStr = 'loser'

                        paraMatchBet.append(paraInputTxs[i-1])                 #将inputTxs中的数据加入到匹配列表，钱包地址暂时为空
                        paraMatchBet.append(paraInputTxs[i])
                        paraMatchBet.append(paraInputTxs[i+1])
                        paraMatchBet.append(tmpStr)
                i -= 4
        print('leave getMatchAndUnmatchBet')  #debug

def reward(paraOutputTxs, paraMatchBet, paraUnMatchBet):#获取所有output交易，判断是否已转入到matchBet对应的地址，如果是，则已完成，否则未完成，进行转账
        print('In reward') #debug
        if paraMatchBet == []:
                return
        i = 0
        k = 0
        tmpOutputTxs = paraOutputTxs.copy()

        for i in range(0, len(paraMatchBet), 4):
                tmpWalletAddr = paraMatchBet[i]
                if paraMatchBet[i+3] == 'winner':
                        try:           
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
                                doXfer(tmpWalletAddr, float(paraMatchBet[i+2])*2*(1-fee), paraUnMatchBet)
        print('leave reward')  #debug

def doXfer(walletAddr, ammount, unmatchBet):        #向胜利者发送XDAG       成功返回交易哈希，失败返回None
        print('In doXfer') #debug
        url = 'http://127.0.0.1:8888'
        body = {"method":"xdag_do_xfer", "params":[{"amount":'%.9f'%(ammount), "address":walletAddr, "remark":"REMARK"}], "id":1}
        resultJson = getXdagRpcJson(url, body)
        if resultJson is not None:
                print(str(datetime.datetime.now()) + ' xfer ' +'%.9f'%(ammount)+' to '+ walletAddr +' succesfully!')
                return resultJson['result'][0]['block']
        else:
                print(str(datetime.datetime.now()) + ' xfer ERROR: Need to xfer ' +'%.9f'%(ammount)+' to '+ walletAddr +'!')
                return None
        print('leave doXfer')  #debug


def calTxVal(paraTxHash):#计算传输哈希值
        s = 0 
        for char in paraTxHash:
                if char.isdigit():
                        s += int(char)
        return s

def refreshPage(paraUnmatchBet, paraMatchBet):
        print('In refreshPage')  #debug
        unmatchBetTableBody = ''
        matchBetTalbeBody = ''
        
        for i in range(0,len(paraUnmatchBet),3):
                unmatchBetTableBody = unmatchBetTableBody + r'<tr><td>' +paraUnmatchBet[i] + r'</td><td>' +paraUnmatchBet[i+1] + r'</td><td>' + str(calTxVal(paraUnmatchBet[i+1])) + r'</td><td>' + paraUnmatchBet[i+2] + r'</td></tr>'

        for i in range(len(paraMatchBet)-4, max(-1,len(paraMatchBet)-44),-4):
                if paraMatchBet[i+3] == 'winner':
                        tdHtml = r'<td style = "color:#D20000">Win '+ '%.9f'%(float(paraMatchBet[i+2])*2*(1-fee)) +r' XDAG</td></tr>'
                else:
                        tdHtml = r'<td>lose</td></tr>'
                matchBetTalbeBody = matchBetTalbeBody + r'<tr><td>' + paraMatchBet[i] + r'</td><td>' + paraMatchBet[i+1] + r'</td><td>' + str(calTxVal(paraMatchBet[i+1])) + r'</td><td>' + paraMatchBet[i+2] + r'</td>'+ tdHtml

        pageFooter = r'<p style="color:#C4CEBF">' + str(datetime.datetime.now()) + r'</p></body></html>'
        f = open(filepath,'w+')         #需增加错误处理
        f.write(htmlCodes.header)
        f.write(unmatchBetTableBody)
        f.write(htmlCodes.tableFooter)
        f.write(htmlCodes.tableHeader)
        f.write(matchBetTalbeBody)
        f.write(htmlCodes.tableFooter)
        f.write(htmlCodes.footer)
        f.write(pageFooter)
        f.close()
        print('leave refreshPage')  #debug

#以下代码用于确认当前区块浏览器中记录的游戏已经清空
totalTxs = 0
while True:     #获取所有交易数据
        print(getAllTxs(allInputTxs, allOutputTxs, WALLETADDR, 1000))
        getLatestTx(txsLatestDict,WALLETADDR, 1000)
        if allInputTxs == []:   #空表示无交易，继续等待
                time.sleep(60)
                continue
        if txsLatestDict['Input'] == allInputTxs[1] and (allOutputTxs == [] or txsLatestDict['Output'] == allOutputTxs[1]):      #证明获取所有交易期间没有增加新的交易，如果不符合，则需重新获取所有交易
                break

#需增加是否达到1000笔交易的上限，如达到，暂停

getMatchAndUnmatchBet(allInputTxs,matchBet,unmatchBet)      #将匹配与未匹配交易进行记录
reward(allOutputTxs,matchBet,unmatchBet)
refreshPage(unmatchBet, matchBet)

oldInputTxTopIndex = 1
oldInputTxTopHash = allInputTxs[1]

del(allInputTxs)
del(allOutputTxs)
print(gc.collect())

while True:#需增加是否达到1000笔交易的上限，如达到，暂停
        time.sleep(180)   #debug 初始120
        #while True:
        del(newAllInputTxs[:])  #清空
        del(newAllOutputTxs[:]) #清空
        print(gc.collect())
        getNewTxs(newAllInputTxs, newAllOutputTxs, WALLETADDR)
                #getLatestTx(txsLatestDict, WALLETADDR)
                #if newAllInputTxs == []:   #空表示无交易，继续等待
                #        continue
                #if txsLatestDict['Input'] == newAllInputTxs[1] and (newAllOutputTxs == [] or txsLatestDict['Output'] == newAllOutputTxs[1]):   #证明获取所有交易期间没有增加新的交易，如果不符合，则需重新获取所有交易
                #        break
        
        oldInputTxTopIndex = newAllInputTxs.index(oldInputTxTopHash)
        if oldInputTxTopIndex == 1:
                continue
        elif oldInputTxTopIndex >= 77: #表示达到获取数据的最大值（ pageSize = 20，77 = (20-1)*4+1 ）
                print('transaction too much! Need to restart!')
                input() #暂停程序
        else:
                print(str(datetime.datetime.now()) + ' New input arrived!')
                print(str(datetime.datetime.now()) + ' ' + str(newAllInputTxs[ 0 : oldInputTxTopIndex - 1]))
                
                time.sleep(10)
                getNewInputTxsWallet(newAllInputTxs, oldInputTxTopIndex - 1)

                getMatchAndUnmatchBet(newAllInputTxs[ 0 : oldInputTxTopIndex - 1], newMatchBet, unmatchBet)      #将新增交易记录到匹配与未匹配交易列表，得到新的匹配列表
                reward([], newMatchBet,unmatchBet)      #由于新的匹配交易，不可能已经被支付过，所以reward第一个参数为空
                for newMatchBetItem in newMatchBet:     #向matchBet列表增加新元素，但是只保留最近30个，新元素在后，老元素在前
                        matchBet.append(newMatchBetItem)
                del(newMatchBet[:])
                if len(matchBet)>40:
                        del(matchBet[0:len(matchBet)-40])
                print(gc.collect())
                refreshPage(unmatchBet, matchBet)       #只有发现有新的交易进入时才刷新页面，减少读写文件次数
        oldInputTxTopHash = newAllInputTxs[1]
        