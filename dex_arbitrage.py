#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 16:06:47 2018

@author: brettwang
"""

#import urllib2
#import urllib
import pywaves as pw 
import time
# set Matcher node to use
#pw.setMatcher(node=u'https://matcher.wavesplatform.com/matcher')
pw.setMatcher(node=u'https://nodes.wavesnodes.com')


### find triangles
data = pw.markets() #get all traded markets with tickers
symbol = pw.symbols()
verifiedPair = [item for item in data if item['symbol']!='']
# get verified pairs with non-zero 24 hour volume
verifiedTradedPair = [item for item in verifiedPair if float(item['24h_priceVolume'])!=0]
# convert to dictionary
verifiedTradedPairDict = {}
for item in verifiedTradedPair:
    verifiedTradedPairDict[item['symbol']]=item
    
# get price asset in verifiedTradedPair
priceAssetSet = set() # ETH WAVES BTC WTRY EUR USD
amountAssetSet = set() 
for item in verifiedTradedPairDict.keys():
    priceAssetSet.add(item.split('/')[1])
    amountAssetSet.add(item.split('/')[0])
# end get price asset in verifiedTradedPair

# get triangle
p = dict().fromkeys(amountAssetSet)
for i in amountAssetSet:
    for j in priceAssetSet:
        if i+'/'+j in verifiedTradedPairDict.keys():
            if p[i] is None:
                p[i] = [j]
            else:
                p[i].append(j)
triangles = []
for k,v in p.items():
    if len(v) == 2:
        if v[0]+'/'+v[1] in verifiedTradedPairDict.keys():
            triangles.append(k+'-'+v[1]+'-'+v[0])
        elif v[1]+'/'+v[0] in verifiedTradedPairDict.keys(): 
            triangles.append(k+'-'+v[0]+'-'+v[1])
    elif len(v) > 2:
        v.remove('BTC')
        for item in v:
            if item+'/'+'BTC' in verifiedTradedPairDict.keys():
                triangles.append(k+'-BTC-'+item)
            else:
                triangles.append(k+'-'+item+'-BTC')
#end get triangle        

### find triangles      

#get ALL symbol and assetID dictionary.
symbolMapping = {}
for item in symbol:
    #symbolMapping[item['symbol']]=pw.Asset(item['assetID'])
    symbolMapping[item['symbol']]=item['assetID']

#only get necessary symbol to create pywaves asset 
assetMapping = {}
symbolSet = set()
for item in triangles:
    symbolSet.add(item.split('-')[0])
    symbolSet.add(item.split('-')[1])
    symbolSet.add(item.split('-')[2])
for item in symbolSet:
    assetMapping[item]=pw.Asset(symbolMapping[item])


#get necessary pairs for triangles
pairs = set()
for item in triangles:
    tmp = item.split('-')
    pairs.add(tmp[0]+'/'+tmp[1])
    pairs.add(tmp[0]+'/'+tmp[2])
    pairs.add(tmp[2]+'/'+tmp[1])

pairMapping = {}
for item in pairs:
    if item not in pairMapping.keys():
        pairMapping[item]=pw.AssetPair(assetMapping[item.split('/')[0]], assetMapping[item.split('/')[1]])

while True:
    print('looping')
    print(time.ctime())    
    price = dict().fromkeys(pairMapping)
    for k,v in pairMapping.items():
        price[k]={}
        tmp1 = v.orderbook()['asks']
        tmp2 = v.orderbook()['bids']
        if (tmp1 != []) and (tmp2 != []):
            price[k]['ask']= tmp1[0]['price']
            price[k]['bid']= tmp2[0]['price']
        else: # if ask or bid orderbook is empty, remove this pair from pairMapping and remove any triangles related to this pair
            pairMapping.pop(k)
            price.pop(k)
            toDeletefromTrianlge = []
            for item in triangles:
                if (item.split('-')[0]+'/'+item.split('-')[1] == k) or (item.split('-')[0]+'/'+item.split('-')[2] == k):
                    toDeletefromTrianlge.append(item)
            while len(toDeletefromTrianlge)!=0:            
                triangles.remove(toDeletefromTrianlge.pop())
                
    # check equilibriunm
    for tri in triangles:
        tmp = tri.split('-')
        x=float(price[tmp[0]+'/'+tmp[1]]['ask'])/(10**assetMapping[tmp[1]].decimals)
        y=float(price[tmp[0]+'/'+tmp[2]]['bid'])/(10**assetMapping[tmp[2]].decimals)
        z=float(price[tmp[2]+'/'+tmp[1]]['bid'])/(10**assetMapping[tmp[1]].decimals)
        if tmp[2]+'/'+tmp[1] == 'EUR/USD':# api error, manual correction 
            z/=(10**6)
        equ = z*y/x
        if equ > 1:
            print(tri)
            print(str(equ))
            #l.append([str(time.ctime()),tri,equ])
            with open('result.txt','a') as f:
                f.write(time.ctime()+',')
                f.write(tri+',')
                f.write(str(equ)+'\n')         