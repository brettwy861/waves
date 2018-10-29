#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 17:50:16 2018

@author: brettwang
"""

import pywaves as pw 
import base64
import time

testNetapi = 'http://52.28.66.217:6869'
mainNetapi = 'http://wavesnode.io:6869'
#token_ID = 'xxxxxxxx'
privkey = ''
#assetDetail = json.load(urllib2.urlopen('http://wavesnode.io:6869/assets/details/'+token_ID))
#token_decimal = 10**assetDetail['decimals']
pw.setNode(mainNetapi, 'mainnet')
myAddress = pw.Address(privateKey=privkey)
#myAsset = pw.Asset(token_ID)
#tx=myAddress.sendAsset(recipient = pw.Address(addr_rec), asset = myAsset, amount=token_amount*token_decimal)


#test succussful!
for t in range(1,50):
    k = [str(j) for j in range(t*100+0,t*100+100)]
    v = [j**2 for j in range(t*100+0,t*100+100)]
    data = []
    for i in range(0,100):
        data.append({
      "key" : k[i],
      "type" : "integer",
      "value" : v[i]})
    myAddress.dataTransaction(data)
    time.sleep(0.5)


myAddress.dataTransaction(data)