import re
import socket
import client.client as cli
from flask import Flask, jsonify
from flask_cors import CORS


STATUS = "Success"
HOST = '127.0.0.1'
port = 10010

app = Flask(__name__)
CORS(app)

name2Wallet_privKey = dict()
name2Wallet_address = dict()
coin2Typesig = dict()

@app.route('/actions/aw/<name>')
def addwallet(name):
   
   print("addWallet function")
   print(name)
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.connect((HOST, port))
   privateKey, address = cli.addWallet(s, name)
   s.close()
   print(privateKey)
   print(address)
   name2Wallet_privKey[name] = privateKey
   name2Wallet_address[name] = address
   return jsonify({'status': STATUS})

#get /actions/<name> data: {name :}
@app.route('/actions/cct/<cointype>')
def createcointype(cointype):
   print("createcointype function")   
   print(cointype)
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.connect((HOST, port))
   typesig = cli.createType(s, cointype)
   s.close()
   coin2Typesig[cointype] = typesig
   return jsonify({'status': STATUS})

#get /actions/<name> data: {name :}
@app.route('/actions/ac/<username>/<cointype>/<amount>')
def addcoin(amount, cointype, username):
   print("addcoin")
   print(username)
   print(cointype)
   print(amount)
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.connect((HOST, port))
   typesig = coin2Typesig[cointype]
   result = cli.addCoin(s, amount, cointype, username, typesig)
   s.close()
   return jsonify({'status': STATUS})

#get /actions/<name> data: {name :}
@app.route('/actions/s/<from_name>/<to_name>/<cointype>/<amount>')
def send(from_name, to_name, cointype, amount):
   print("send function")
   print(from_name)
   print(to_name)
   print(cointype)
   print(amount)
   sig = "Success"
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.connect((HOST, port))
   balance = cli.sendCoin(s, from_name, to_name, cointype, amount, sig.encode('utf-8'))
   s.close()
   return jsonify({'status': STATUS})

#get /actions/<name> data: {name :}
@app.route('/actions/gb/<username>')
def getbalance(username):
   print("getbalance function")
   print(username)

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.connect((HOST, port))
   
   balance = cli.getBalance(s, username)
   s.close()
   return jsonify({'balance': balance})

"""
#post /store data: {name :}
@app.route('/post' , methods=['POST'])
def create_store():
   print()
#get /store/<name> data: {name :}
@app.route('/store/<string:name>')
def get_store(name):
   return jsonify({"name": name})
#get /store
@app.route('/store')
def get_stores():
   print("hello flask, your route is /store")
   return jsonify({'message': 'store not found'})
#post /store/<name> data: {name :}/item
@app.route('/store/<string:name>/item' , methods=['POST'])
def create_item_in_store(name):
    pass
#get /store/<name>/item data: {name :}/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    pass
"""

app.run(port=5000, debug=True)