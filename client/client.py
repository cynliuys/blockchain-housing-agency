'''
1.Create type
    (1)Send 'Get key pair'
    (2)Send 'CoinType'
    (3)Recv 'Sign'

2.Add wallet
    (1)Send 'Create wallet name'
    (2)Recv 'PrivateKey'
    (3)Recv 'address'

3.Add coin
    (1)Send 'New request'
    (2)Send 'subsidy cointype name typesig (addcoin)'

4.Send coin
    (1)Send 'New request'
    (2)Send 'from_name to_name cointype amount sig (send)'
    (3)Return the balance of from_name and to_name

5.Get balance 
    (1)Send 'get balance name'
    (2)Return the balance of the name 

'''
import socket
import time
import codecs
import binascii
import ecdsa

HOST = ''
port = 10010

def createType(s, coinType):
    s.send(b'Get key pair')
    time.sleep(2)
    s.send(coinType.encode('utf-8'))
    sign = s.recv(2048)
    return sign


def addWallet(s, name):
    data = 'Create wallet ' + name
    s.send(data.encode('utf-8'))
    privateKey = s.recv(2048)
    if privateKey != b'False' :
        address = s.recv(2048).decode('utf-8')
        return privateKey, address
    return 0, 0


def addCoin(s, subsidy, cointype, name, typesig):
    data = str(subsidy).encode('utf-8') + b'   ' + cointype.encode('utf-8') + b'   ' + \
                name.encode('utf-8') + b'   ' + typesig + b'   (addcoin)'
    s.send(b'New request')
    time.sleep(1)
    s.send(data)
    result = s.recv(2048).decode('utf-8')
    return result



def sendCoin(s, from_name, to_name, cointype ,amount ,sig):
    s.send(b'New request')
    data = from_name.encode('utf-8') + b'   ' + to_name.encode('utf-8') + b'   ' + \
           cointype.encode('utf-8') + b'   ' + str(amount).encode('utf-8') + b'   ' +\
           sig + b'   ' + b'(send)'
    s.send(data)
    balance = s.recv(2048)
    return balance.decode('utf-8')


def getBalance(s, name):
    data = 'get balance ' + name
    s.send(data.encode('utf-8'))
    balance = s.recv(2048)
    return balance


if __name__ == '__main__':

    #Create Wallet --name Cynthia
    ip = input()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    privateKey1, addr1 = addWallet(s, 'Cynthia')
    if privateKey1 != 0:
        print('create wallet Cynthia success')
    else:
        print ('create wallet Cynthia failed !')

    #Create Wallet --name Pierre
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    ip = input()
    privateKey2, addr2 = addWallet(s, 'Pierre')
    if privateKey2 != 0:
        print('create wallet Pierre success')
    else:
        print ('create wallet Pierre failed !')

    #Get Type Signature --cointype Di_Bao
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    ip = input()
    sign1 = createType(s, 'Di_Bao')
    print("Get Di_Bao signature")

    #Add Coin --name Cynthia --cointype Di_Bao --subsidy 100
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    ip = input()
    result = addCoin(s, 100, 'Di_Bao', 'Cynthia', sign1)
    print(result)

    #Send --from Cynthia --to Pierre --cointype Di_Bao --amount 10
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    ip = input()
    sk = ecdsa.SigningKey.from_string(privateKey1, curve=ecdsa.SECP256k1)
    sig = sk.sign('yes'.encode('UTF-8'))
    balance = sendCoin(s, 'Cynthia', 'Pierre', 'Di_Bao' ,10 ,sig)
    print('Cynthia balance :\n'+ balance)

    #Get Balance --name Cynthia
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    ip = input()
    balance = getBalance(s, 'Cynthia')
    print('Cynthia balance :\n'+ balance.decode('utf-8'))

    #Send --from Cynthia --to Danny --cointype Di_Bao --amount 10
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    ip = input()
    sk = ecdsa.SigningKey.from_string(privateKey1, curve=ecdsa.SECP256k1)
    sig = sk.sign('yes'.encode('UTF-8'))
    balance = sendCoin(s, 'Cynthia', 'Danny', 'Di_Bao' ,10 ,sig)
    print('Send '+ balance)

    #Create Wallet --name Danny
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    ip = input()
    privateKey3, addr3 = addWallet(s, 'Danny')
    if privateKey3 != 0:
        print('create wallet Danny success')
    else:
        print ('create wallet Danny failed !')

    #Send --from Cynthia --to Danny --cointype Di_Bao --amount 10
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    ip = input()
    sk = ecdsa.SigningKey.from_string(privateKey1, curve=ecdsa.SECP256k1)
    sig = sk.sign('yes'.encode('UTF-8'))
    balance = sendCoin(s, 'Cynthia', 'Danny', 'Di_Bao' ,10 ,sig)
    print('Cynthia balance :\n'+ balance)

    #Get Type Signature --cointype 7_chi
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    ip = input()
    sign2 = createType(s, '7_chi')
    print("Get 7_chi signature")

    #Add Coin --name Pierre --cointype 7_chi --subsidy 100
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    ip = input()
    result = addCoin(s, 100, '7_chi', 'Pierre', sign2)
    print(result)

    #Send --from Pierre --to Danny --cointype 7_chi --amount 20
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    ip = input()
    sk = ecdsa.SigningKey.from_string(privateKey2, curve=ecdsa.SECP256k1)
    sig = sk.sign('yes'.encode('UTF-8'))
    balance = sendCoin(s, 'Pierre', 'Danny', '7_chi' ,20 ,sig)
    print('Pierre balance :\n'+ balance)

    #Get Balance --name Cynthia
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    ip = input()
    balance = getBalance(s, 'Cynthia')
    print('Cynthia balance :\n'+ balance.decode('utf-8'))

    #Get Balance --name Pierre
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    ip = input()
    balance = getBalance(s, 'Pierre')
    print('Pierre balance :\n'+ balance.decode('utf-8'))

    #Get Balance --name Danny
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    ip = input()
    balance = getBalance(s, 'Danny')
    print('Danny balance :\n'+ balance.decode('utf-8'))






    '''



    time.sleep(1)

    # Reconnect
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    print("Step2 : addWallet")
    privateKey1, addr1 = addWallet(s, 'Cynthia')
    if privateKey1 != 0:
        print('\t-add wallet Cynthia success')
    else:
        print ('\t-add wallet Cynthia failed !')

    # Reconnect
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    privateKey2, addr2 = addWallet(s, 'Pierre')
    if privateKey2 != 0:
        print('\t-add wallet Pierre success')
    else:
        print ('\t-add wallet Pierre failed !')
    time.sleep(1)

    # Reconnect
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    privateKey3, addr3 = addWallet(s, 'Cynthia')
    if privateKey3 != 0:
        print('\t-add wallet Cynthia success')
    else:
        print ('\t-add wallet Cynthia failed !')
    time.sleep(1)

    # Reconnect
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    print("Step3 : addCoin")
    result = addCoin(s, 50, 'QQ', 'Cynthia', sign1)
    print(result)
    time.sleep(2)

    # Reconnect
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    result = addCoin(s, 50, 'RR', 'Pierre', sign2)
    print(result)
    time.sleep(1)

    # Reconnect
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    print("Step4 : sendCoin")
    sk = ecdsa.SigningKey.from_string(privateKey1, curve=ecdsa.SECP256k1)
    sig = sk.sign('yes'.encode('UTF-8'))
    balance = sendCoin(s, 'Cynthia', 'Pierre', 'QQ' ,10 ,sig)
    print('Cynthia balance :\n'+ balance)
    time.sleep(1)

    # Reconnect
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    sk = ecdsa.SigningKey.from_string(privateKey2, curve=ecdsa.SECP256k1)
    sig = sk.sign('yes'.encode('UTF-8'))
    balance = sendCoin(s, 'Danny', 'Cynthia', 'RR' ,20 ,sig)
    print('Pierre balance :\n'+ balance)
    time.sleep(1)


    # Reconnect
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    print("step5: ask for balance")
    A_balance = getBalance(s, 'Cynthia')

    # Reconnect
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    B_balance = getBalance(s, 'Pierre')
    print('Cynthia balance :\n'+ A_balance.decode('utf-8'))
    print('Pierre balance :\n'+ B_balance.decode('utf-8'))
    '''
    s.close()


