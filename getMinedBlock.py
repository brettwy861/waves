#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 18:50:54 2018

@author: brettwang
"""


import requests


addr = 'xxxxxx'
endPoint = 'http://wavesnode.io:6869/blocks/'
#req0 = Request(endPoint+'height',headers={'User-Agent': 'Mozilla/5.0'}) this is for my mac py
req1 = requests.get(endPoint+'height',headers={'User-Agent': 'Mozilla/5.0'})
current_height = req1.json()['height']

minedBlock = []
counter = 1
for i in range(current_height,0,-1):
    req = requests.get(endPoint+'headers/at/'+str(i),headers={'User-Agent': 'Mozilla/5.0'})
    if req.json()['generator'] == addr:
        minedBlock.append(req.json())
        counter -= 1
        print('find one block')
    if counter<=0:
        break
    
#1100205
#1085013
#1068742
#1057108