#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 13:54:36 2018

@author: brettwang
"""
"""
The maximum number of recipients in a single transaction is 100. 
There is no minimum recipient number. 
You can create a transaction with one or even zero recipients. 
In addition, restrictions that apply to Transfers apply here as well,
such as you cannot send negative amount and cannot send more than you have on your account.
Other than that, we've decided not to put any restrictions on transactions that are harmless,
even if they may seem against common sense. For example, transfers to self are allowed,
as well as zero valued transfers. In the recipients list, a recipient can occur several times,
this is not considered an error.
"""

"""
Proofs
In order to prepare for the upcoming Smart Accounts feature, 
Mass Transfer transaction has the signature field replaced with an array of so called "proofs". 
Proofs are an alternative way to authorize the transaction that is more flexible than signatures
and enables smart contracts such as multisig and atomic swap. 
Each proof is a Base58 encoded byte string and can be a signature, a secret, or anything else – 
the semantics of a proof is dictated by the smart contract that interprets it. 
There can be up to 8 proofs at most 64 bytes each.

Now until smart accounts are implemented and activated, 
the only proof that is actually used is the transaction signature. 
It should be the very first element in the proofs array, 
while all the other elements are currently ignored.
"""

#import urllib2
#import urllib
#import json
import pywaves as pw 
import sys


def main(argv):
    if len(argv) != 3:
        print('The correct format is:')
        print('python airdrop.py addressFile assetID privateKey\n')
        print('addressFile is the name of file that contains N lines (N<=100), \n each line starts with a valid waves wallet address and then \n the amount of asset to airdrop, separated by a space\n')
        print('assetID is the assetID of the asset you want to airdrop, that is within your wallet\n')
        print('privateKey is the private key to your wallet address\n')
    else:
        addressFile=sys.argv[1]
        token_ID=sys.argv[2]
        privkey=sys.argv[3]
        #token_ID = 'xxxxxxxxx''
        #assetDetail = json.load(urllib2.urlopen('http://wavesnode.io:6869/assets/details/'+token_ID))
        #token_decimal = 10**assetDetail['decimals']
        pw.setNode('http://wavesnode.io:6869', 'mainnet')
        myAddress = pw.Address(privateKey=privkey)
        myAsset = pw.Asset(token_ID)
        #tx=myAddress.sendAsset(recipient = pw.Address(addr_rec), asset = myAsset, amount=token_amount*token_decimal)
        transfers = []
        with open(addressFile,'r') as f:
            for line in f:
                addr = line.split(' ')[0]
                amount = line.split(' ')[1].rstrip("\n")
                transfers.append({'recipient':addr,'amount':int(amount)})   
        if len(transfers)<100:
            tx=myAddress.massTransferAssets(transfers, myAsset, timestamp=0)
            if 'error' not in tx.keys():
                print('Airdrop was successful. check the transaction detail at: ')
                print('http://wavesexplorer.com/tx/'+tx['id'])
            else:
                print(tx['message'])
        else:
            print('Airdrop was not successful! Limited to maximum of 100 transactions per mass transfer')
if __name__ == "__main__":
   main(sys.argv[1:])

# python airdrop.py addressFile AssetID privateKey 