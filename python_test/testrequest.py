#!/usr/bin/python
# # -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup  

vbSalePrice = []
vBSaleVolumne = []
vbBuyPrice = []
vbBuyVolumn = []
bbxSalePrice = []
bbxSaleVolumn = []
bbxBuyPrice = []
bbxBuyVolumn = []
'''
res = requests.get('http://vbitex.com/Home/Qcorders/index/currency/XDAG.html')
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text,"html.parser")

vbTagTableBuy = soup.find(id="coinbuylist")
for tagPrice in vbTagTableBuy.find_all(onclick="getbuy(this);"):    
    vbBuyPrice.append(float(tagPrice.string))

for tagVolumn in vbTagTableBuy.find_all(onclick="buynum(this);"):
    vbBuyVolumn.append(int(tagVolumn.string))
    
print(vbBuyPrice)
print(vbBuyVolumn)

vbTagTableSale = soup.find(id="coinsalelist")
for tagPrice in vbTagTableSale.find_all(onclick="getsell(this)"):    
    vbSalePrice.append(float(tagPrice.string))

for tagVolumn in vbTagTableSale.find_all(onclick="sellnum(this)"):
    vBSaleVolumne.append(int(tagVolumn.string))

print(vbSalePrice)
print(vBSaleVolumne)
'''


res = requests.get('https://www.bbx.com/exchange?coinPair=XDAG/ETH')
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text,"html.parser")
bbxTagTableSale = soup.find_all("div", attrs={"class": "data-list-table"})
#for tagPrice in bbxTagTableBuy.find_all(class_="list-td"):    
#    vbBuyPrice.append(float(tagPrice.string))

print(res.text)

'''
for tag in soup.find_all('div', class_='info'):    
   # print tag  
    m_name = tag.find('span', class_='title').get_text()        
    m_rating_score = float(tag.find('span',class_='rating_num').get_text())          
    m_people = tag.find('div',class_="star")  
    m_span = m_people.findAll('span')  
    m_peoplecount = m_span[3].contents[0]  
    m_url=tag.find('a').get('href')  
    print( m_name+"        "  +  str(m_rating_score)   + "           " + m_peoplecount + "    " + m_url )   
'''