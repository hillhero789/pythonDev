#!/usr/bin/python
# # -*- coding: utf-8 -*-
import requests
import time
import json
import htmlCodes_bootstrap
import htmlCodes_bootstrap_en
import datetime
import gc

fee = 0.0
filepath = r'/var/www/html/index.html'
filepath_en = r'/var/www/html/index_en.html'
EXPLORER_URL = r'https://explorer.xdag.io/api/block/'  
#以上参数需要提前设置

unmatchBet = []         #[wallet, 见证块哈希，数量，...]  //每小时向前10名赠送 (数量<1000?数量:1000) * .001。
matchBet = []           #[wallet, 见证块哈希，数量，winner or loser，...]
newMatchBet = []        
newAllInputTxs = []     #获取最新输入交易 [wallet, 见证块哈希，数量，时间]                               新数据在前，旧数据在后
newAllOutputTxs = []    #获取最新输出交易 [wallet, 见证块哈希，数量，时间]  

WALLETADDR = 'fKVvnRLb163cw+W0kIjlJxMIp44yirQZ'       

def getXdagRpcJson(url, body, attemptTimes = 20):
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
                except:
                        connError += 1
                        print(str(datetime.datetime.now()) +' Connection error for '+ str(connError) +' times!')
                        time.sleep(3)
                        if connError >= attemptTimes:
                                print(str(datetime.datetime.now()) +' conn ERROR!')
                                return None
        return resultJson

def getBlockJson(addr, attemptTimes = 10):
        errorCounter = 0
        connError = 0
        while True:
                try:
                        resp = requests.get(EXPLORER_URL + addr)
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
                except:
                        connError += 1
                        print(str(datetime.datetime.now()) +' Connection error for '+ str(connError) +' times!')
                        time.sleep(3)
                        if connError >= attemptTimes:
                                print(str(datetime.datetime.now()) +' conn ERROR!')
                                return None
        return resultJson

def log(logContent):
        f = open('./log.txt','a+')         #需增加错误处理
        f.write(logContent + '\n')
        f.close()

def getBlockInfo(txHash):#根据传输哈希获取对应的钱包地址，direction 表示交易传输方向
        ret = {'input':'','output':'','fee':''}
        resultJson = getBlockJson(txHash)
        if resultJson is None:
                input("Error:get data error, resultJson is none")
        for blockItem in resultJson['block_as_transaction']:
                if blockItem['direction'] == 'fee':
                        ret['fee'] = blockItem['address']      
                elif blockItem['direction'] == 'input':
                        ret['input'] = blockItem['address']
                elif blockItem['direction'] == 'output':
                        ret['output'] = blockItem['address']
        del(resultJson)
        gc.collect()
        return ret    

def getNewTxs(paraInputTxs, paraOutputTxs, walletAddr):# 与getAllTxs区别在于先不填写钱包地址
        resultJson = getBlockJson(walletAddr)
        if resultJson is not None:
                for r in resultJson['block_as_address']:
                        if r['direction'] == 'input':
                                paraInputTxs.append('')                 #为减少调用requests.post，提高性能，在putWalletAndWitness中填入参数
                                paraInputTxs.append(r['address'])       #此时地址仍未被替换为 见证块哈希，在putWalletAndWitness中填入
                                paraInputTxs.append(r['amount'])
                                paraInputTxs.append(r['time'])
                        else:
                                paraOutputTxs.append('')                #为减少调用requests.post，提高性能，在putWalletAndWitness中填入参数
                                paraOutputTxs.append(r['address'])      #此时地址仍未被替换为 见证块哈希，在putWalletAndWitness中填入
                                paraOutputTxs.append(r['amount'])
                                paraOutputTxs.append(r['time'])
        del(resultJson)
        gc.collect()

def putWalletAndWitness(paraTxs, endIndex, direction='input'):        #获取钱包地址和见证块哈希，并填入到paraTxs
        tmpBlockInfo = {}
        ret = paraTxs[1]
        for i in range(0, endIndex, 4):
                tmpBlockInfo = getBlockInfo(paraTxs[i+1])
                paraTxs[i] = tmpBlockInfo[direction]         #wallet
                paraTxs[i+1] = tmpBlockInfo['fee']         #witness hash
                time.sleep(1)
        return  ret

def getMatchAndUnmatchBet(paraInputTxs, paraMatchBet, paraUnmatchBet):#paraInputTxs为输入交易列表
        tmpHash = ''
        tmpWallet = ''
        tmpStr = 'loser'
        i = len(paraInputTxs) - 3        # i-1是钱包地址，i 是见证块哈希（ID），i+1 是数量   计算出已经完成的bet，和未完成的bet
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
                        tmpWallet = paraUnmatchBet.pop(j-2)     #将原来在不匹配列表(挂单)中的数据加入到匹配列表
                        tmpHash = paraUnmatchBet.pop(j-2)     

                        paraMatchBet.append(tmpWallet)          
                        paraMatchBet.append(tmpHash)
                        paraMatchBet.append(paraUnmatchBet.pop(j-2))
                        if (calTxVal(tmpHash) + calTxVal(paraInputTxs[i])) % 2 == 0 : #偶数挂单者输，奇数吃单者输
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

def rewardPerHour(paraUnMatchBet):
        xferAmountBase = 0.0
        if paraUnMatchBet == []:
                return
        for i in range(0, len(paraUnMatchBet), 3):
                if i > 27:
                        break
                xferAmountBase = float(paraUnMatchBet[i+2])
                if  xferAmountBase > 1000.0:
                        xferAmountBase = 1000.0
                doXfer(paraUnMatchBet[i], xferAmountBase*0.001, 'http://127.0.0.1:8888')

def reward(paraOutputTxs, paraMatchBet):#获取所有output交易，判断是否已转入到matchBet对应的地址，如果是，则已完成，否则未完成，进行转账
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
                                                tmpOutputTxs.pop(k)             #防止一个钱包相同金额赢了多次，不给转账
                                                tmpOutputTxs.pop(k)
                                                tmpOutputTxs.pop(k)
                                                tmpOutputTxs.pop(k)
                                                break
                                        else:
                                                k = tmpOutputTxs.index(tmpWalletAddr, k+1)#如果钱包地址一致，金额不一致，则继续向后查找，找不到了，则转账        
                        except ValueError:
                                doXfer(tmpWalletAddr, float(paraMatchBet[i+2])*2*(1-fee))


def doXfer(walletAddr, amount, url = 'http://127.0.0.1:8878'):        #向胜利者发送XDAG       成功返回交易哈希，失败返回None
        #print('In doXfer') #debug
        #url = 'http://127.0.0.1:8888'
        body = {"method":"xdag_do_xfer", "params":[{"amount":'%.9f'%(amount), "address":walletAddr, "remark":"REMARK"}], "id":1}
        resultJson = getXdagRpcJson(url, body, 2)
        if resultJson is not None:
                ret = resultJson['result'][0]['block']
                del(resultJson)
                gc.collect()
                print(str(datetime.datetime.now()) + ' xfer ' +'%.9f'%(amount)+' to '+ walletAddr +' succesfully!')
                return ret
        else:
                del(resultJson)
                gc.collect()
                print(str(datetime.datetime.now()) + ' xfer ERROR: Need to xfer ' +'%.9f'%(amount)+' to '+ walletAddr +'!')
                log(str(datetime.datetime.now()) + ' xfer ERROR: Need to xfer ' +'%.9f'%(amount)+' to '+ walletAddr +'!')
                return None


def calTxVal(paraTxHash):#计算传输哈希值
        s = 0 
        for char in paraTxHash:
                if char.isdigit():
                        s += int(char)
        return s

def refreshPage(paraUnmatchBet, paraMatchBet):
        unmatchBetTableBody = ''
        matchBetTalbeBody = ''
        
        for i in range(0,len(paraUnmatchBet),3):
                unmatchBetTableBody = unmatchBetTableBody + r'<tr><td>' +paraUnmatchBet[i+2] + r'</td><td>' + str(calTxVal(paraUnmatchBet[i+1])) + r'</td><td>' + paraUnmatchBet[i+1] + r'</td><td>' + paraUnmatchBet[i] + r'</td></tr>'

        for i in range(len(paraMatchBet)-4, max(-1,len(paraMatchBet)-84),-4):   
                if paraMatchBet[i+3] == 'winner':
                        tdHtml = r'<td style = "color:#D20000">Win '+ '%.9f'%(float(paraMatchBet[i+2])*2*(1-fee)) +r'</td>'
                else:
                        tdHtml = r'<td>lose</td>'
                matchBetTalbeBody = matchBetTalbeBody + r'<tr>' + tdHtml + r'<td>' + paraMatchBet[i+2] + r'</td><td>' + str(calTxVal(paraMatchBet[i+1])) + r'</td><td>' + paraMatchBet[i+1] + r'</td><td>' + paraMatchBet[i] + r'</td></tr>'

        pageFooter = r'<p style="color:#FFFFFF">' + str(datetime.datetime.now()) + r'</p></div></body></html>'
        f = open(filepath,'w+')         #需增加错误处理
        f.write(htmlCodes_bootstrap.header)
        f.write(unmatchBetTableBody)
        f.write(htmlCodes_bootstrap.tableFooter)

        f.write(htmlCodes_bootstrap.tableHeader)
        f.write(matchBetTalbeBody)
        f.write(htmlCodes_bootstrap.tableFooter)

        f.write(htmlCodes_bootstrap.footer)
        f.write(pageFooter)
        f.close()
        #---------------------------------English page--------------------------------------
        f = open(filepath_en,'w+')         #需增加错误处理
        f.write(htmlCodes_bootstrap_en.header_en)
        f.write(unmatchBetTableBody)
        f.write(htmlCodes_bootstrap_en.tableFooter_en)

        f.write(htmlCodes_bootstrap_en.tableHeader_en)
        f.write(matchBetTalbeBody)
        f.write(htmlCodes_bootstrap_en.tableFooter_en)

        f.write(htmlCodes_bootstrap_en.footer_en)
        f.write(pageFooter)
        f.close()

        del(unmatchBetTableBody)
        del(matchBetTalbeBody)
        gc.collect()


#------------------------------------------程序开始------------------------------------------
doItOnce = True
counter = 0
oldInputTxTopIndex = 1
oldOutputTxTopIndex = 1
oldInputTxTopHash = r''   
oldOutputTxTopHash = r''        #主要用于在reward()检查matchBet列表是否已经reward过了。
while True:#需增加是否达到1000笔交易的上限，如达到，暂停
        del(newAllInputTxs[:])  #清空
        del(newAllOutputTxs[:]) #清空
        gc.collect()
        time.sleep(60)   # 60

        counter = counter + 1
        if counter == 60:
                rewardPerHour(unmatchBet)
                counter = 0

        getNewTxs(newAllInputTxs, newAllOutputTxs, WALLETADDR)
        
        if newAllInputTxs != []:
                if oldInputTxTopHash != '':     #允许从非新地址开始启动游戏
                        try:
                                oldInputTxTopIndex = newAllInputTxs.index(oldInputTxTopHash)
                        except ValueError:
                                input("Error: can not find oldInputTxTopHash in newAllInputTxs")
                else:
                        oldInputTxTopIndex = len(newAllInputTxs)+1

        if oldInputTxTopIndex != 1:
                print(str(datetime.datetime.now()) + ' New input arrived!')
                print(str(datetime.datetime.now()) + ' ' + str(newAllInputTxs[ 0 : oldInputTxTopIndex - 1]))
                
                time.sleep(1)  #将连续两次调用rpc的时间稍微隔开
                oldInputTxTopHash = putWalletAndWitness(newAllInputTxs, oldInputTxTopIndex - 1) #修改 newAllInputTxs，同时返回其第一个元素的 交易哈希，以便下次搜索用
                getMatchAndUnmatchBet(newAllInputTxs[ 0 : oldInputTxTopIndex - 1], newMatchBet, unmatchBet)      #将新增交易记录到匹配与未匹配交易列表，得到新的匹配列表
                
                if doItOnce is True:    #仅重新启动时需要执行此部分代码
                        if newAllOutputTxs != []:
                                if oldOutputTxTopHash != '':    #允许从非新地址开始启动游戏
                                        try:
                                                oldOutputTxTopIndex = newAllOutputTxs.index(oldOutputTxTopHash)
                                        except ValueError:
                                                input("Error: can not find oldOutputTxTopHash in newAllOutputTxs")
                                else:
                                        oldOutputTxTopIndex = len(newAllOutputTxs)+1

                                if oldOutputTxTopIndex != 1:
                                        oldOutputTxTopHash = putWalletAndWitness(newAllOutputTxs, oldOutputTxTopIndex - 1,'output')

                                reward(newAllOutputTxs[0:oldOutputTxTopIndex - 1], newMatchBet)      #重新启动避免重复发放奖励
                        doItOnce = False
                else:
                        reward([], newMatchBet)#非重启，则新匹配的交易，不可能已经被支付过，所以reward第一个参数为空
                        
                for newMatchBetItem in newMatchBet:     #向matchBet列表增加新元素，但是只保留最近30个，新元素在后，老元素在前
                        matchBet.append(newMatchBetItem)
                del(newMatchBet[:])
                if len(matchBet)>80:            #显示最近10对交易 10 * 2 * 4 = 80
                        del(matchBet[0:len(matchBet)-80])
                gc.collect()
                refreshPage(unmatchBet, matchBet)       #只有发现有新的交易进入时才刷新页面，减少读写文件次数