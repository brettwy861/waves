#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 21:26:50 2018

@author: brettwang
"""
import urllib2
#import urllib
import json
import pywaves as pw 
import time

token_ID = 'xxxxxxx' # nova token
presale_wallet_addr = ''
privkey = ''
assetDetail = json.load(urllib2.urlopen('http://wavesnode.io:6869/assets/details/'+token_ID))
token_decimal = 10**assetDetail['decimals']
# set Matcher node to use
#pw.setMatcher(node=u'https://matcher.wavesplatform.com/matcher')
pw.setMatcher(node=u'https://nodes.wavesnodes.com')
myAddress = pw.Address(privateKey=privkey)

# post a buy order, test successful
BTC = pw.Asset('8LQW8f7P5d5PZM7GtZEBgaqRPGSzS3DfPuiXrURJ4AJS')
ETH = pw.Asset('474jTeYx2r2Va35794tCScAXWJG9hU2HcgxzMowaZUnu')
token_decimal=ETH.decimals
ETH_BTC = pw.AssetPair(ETH, BTC)
t0=time.time()
UnitPrice = 0.0505
AmountAssetToBuy = 0.001
myBuyOrder = myAddress.buy(assetPair = ETH_BTC, amount = AmountAssetToBuy*10**ETH_BTC.asset1.decimals, price = UnitPrice*10**ETH_BTC.asset2.decimals)
t1=time.time()
dt = t1-t0

# post a sell order , test successful
NOVA = pw.Asset(token_ID)
BTC = pw.Asset('8LQW8f7P5d5PZM7GtZEBgaqRPGSzS3DfPuiXrURJ4AJS')
token_decimal = NOVA.decimals
NOVA_BTC = pw.AssetPair(NOVA, BTC)
t0=time.time()#time monitor
AmountAssetToSell = 600
UnitPrice = 0.0001
mySellOrder = myAddress.sell(assetPair = NOVA_BTC, amount = AmountAssetToSell*10**NOVA_BTC.asset1.decimals, price = UnitPrice*10**NOVA_BTC.asset2.decimals)
t1=time.time()#time monitor
dt = t1-t0

# post a buy order using Waves as price asset, test successful
NOVA = pw.Asset(token_ID)
token_decimal = NOVA.decimals
NOVA_WAVES = pw.AssetPair(NOVA, pw.WAVES)
t0=time.time()#time monitor
AmountAssetToBuy = 100
UnitPrice = 0.000001
myBuyOrder = myAddress.buy(assetPair = NOVA_WAVES, amount = AmountAssetToBuy*10**NOVA_WAVES.asset1.decimals, price = UnitPrice*(10**8))
t1=time.time()#time monitor
dt = t1-t0

# cancel an order, test successful
myBuyOrder.cancel()
mySellOrder.cancel()
# or
myAddress.cancelOrder(NOVA_WAVES, myBuyOrder)
myAddress.cancelOrder(NOVA_BTC, mySellOrder)
myAddress.cancelOrderByID(assetPair=NOVA_BTC,orderId=mySellOrder.orderId)
"""
Address Class

pywaves.Address(address, publicKey, privateKey, seed) Creates a new Address object

attributes:
address
publicKey
privateKey
seed

methods:

tradableBalance(assetPair) #get tradable balance for the specified asset pair
buy(assetPair, amount price, maxLifetime=30*86400, matcherFee=DEFAULT_MATCHER_FEE, timestamp=0) #post a buy order
sell(assetPair, amount, price, maxLifetime=30*86400, matcherFee=DEFAULT_MATCHER_FEE, timestamp=0) #post a sell order
cancelOpenOrders(assetPair) #cancel all open orders for the specified asset pair
cancelOrderByID(assetPair,orderId) #cancel order with assetPair and orderId
cancelOrder(assetPair, order) #cancel an order
getOrderHistory(assetPair) #get order history for the specified asset pair
deleteOrderHistory(assetPair) #delete order history for the specified asset pair
"""

"""
AssetPair Class

pywaves.AssetPair(asset1, asset2) Creates a new AssetPair object with 2 Asset objects

attributes:
asset1
asset2

methods:
orderbook() get order book
ticker() get ticker with 24h ohlcv data
last() get traded price
open() get 24h open price
high() get 24h high price
low() get 24h low price
close() get 24h close price (same as last())
vwap() get 24h vwap price
volume() get 24h volume
priceVolume() get 24h price volume
trades(n) get the last n trades
trades(from, to) get the trades in from/to interval
candles(timeframe, n) get the last n candles in the specified timeframe
candles(timeframe, from, to) get the candles in from/to interval in the specified timeframe
"""

"""
Order Class

pywaves.Order(orderId, assetPair, address='') Creates a new Order object

attributes:
status
orderId
assetPair
address
matcher
matcherPublicKey

methods:
status() returns current order status cancel() cancel the order
"""

### find triangles
data = pw.markets() #get all traded markets with tickers
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
            triangles.append(k+'-BTC-'+item)
#end get triangle        
### find triangles      
    