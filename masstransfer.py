import urllib2
#import urllib
import json
import pywaves as pw 

 
token_ID = 'xxxxxxx'
presale_wallet_addr = ''
privkey = ''
assetDetail = json.load(urllib2.urlopen('http://5.189.182.6:6869/assets/details/'+token_ID))
token_decimal = 10**assetDetail['decimals']
pw.setNode('http://5.189.182.6:6869', 'mainnet')
myAddress = pw.Address(privateKey=privkey)
myAsset = pw.Asset(token_ID)
#tx=myAddress.sendAsset(recipient = pw.Address(addr_rec), asset = myAsset, amount=token_amount*token_decimal)
transfers = []
with open('addressList.txt','r') as f:
    for line in f:
        addr = line.split(' ')[0]
        amount = line.split(' ')[1].rstrip("\n")
        transfers.append({'recipient':addr,'amount':int(amount)})



transfers = [{ 'recipient': 'xxxxx', 'amount': 1000 },
             { 'recipient': 'xxxxx', 'amount': 2000 },
             {'recipient': 'xxxxx', 'amount': 3000 },
             { 'recipient': 'xxxxx', 'amount': 4000 }]

        

myAddress.massTransferAssets(transfers, myAsset, timestamp=0)
#test succussful!


