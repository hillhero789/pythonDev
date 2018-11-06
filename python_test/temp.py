#!/usr/bin/python
# # -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup  
res = requests.get('https://explorer.xdag.io/block/SNiOG7aUUyZ3QmSl87T0CsUezb5C5l5X')
res.encoding = 'utf-8'

soup = BeautifulSoup(res.text,"html.parser")
'''
td1 = soup.tbody.td

for tdIndex in td1.next_siblings:
        if tdIndex.name =="td": 
                print(tdIndex.get_text())
'''
tds = soup.tbody.find_all('td')
for td2 in tds:
        print(td2.get_text())

#dict = {"aa":88,"bb":77,"cc":99}
#for x,y in dict.items():
#    print(x,y)

#set1 = set([1,2,3,4,5,3,4,5])
#print(set1)
#set2 = set((1,2,3,3,2,1))
#print(set2)
#set3 = set({1:"good", 2:"nice"})
#print(set3)
'''
orders = {'BUY':{'price':[0.11,0.10,0.09],'volumn':[100,99,98]},'SELL':{'price':[0.12,0.13,0.14],'volumn':[1000,990,908]}}

for buyOrders in orders.get('BUY'):
    for aa,bb in buyOrders.items():
        print(aa,bb)
'''    
#函数返回VB当前交易 {'BUY':[price1,...]}
#def getVbOrders():

