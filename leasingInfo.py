#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 22:18:39 2018

@author: brettwang
"""

import requests


addr = 'xxxxxxx'
endPoint = 'http://wavesnode.io:6869'

def getActivelease(addr):
    req1 = requests.get(endPoint+'/leasing/active/'+addr,headers={'User-Agent': 'Mozilla/5.0'})
    activeLease = req1.json()
    return activeLease
#req0 = Request(endPoint+'height',headers={'User-Agent': 'Mozilla/5.0'}) this is for my mac py

def getAllleasesbyAddress(activeLease, addr):
    addressDict = {}
    for item in activeLease:
        if item['sender'] not in addressDict.keys():
            addressDict[item['sender']]=item['amount']
        else:
            addressDict[item['sender']]+=item['amount']
    sortedDict = sorted(addressDict.items(),key = lambda d:d[1],reverse=True)
    return sortedDict

def getLeasesbyAddress(activeLease, addr):
    result = []
    for item in activeLease:
        if item['sender'] == addr:
            result.append(item)
    return result

def effectiveLeasebalanceSinceT1(activeLease,t1,addr):
    result = 0
    for item in activeLease:
        if item['sender'] == addr and (int(item['timestamp']) <= int(t1)): #only consider full month
            result+=item['amount']