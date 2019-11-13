import socket
import binascii
import ecdsa
import base58
import os
HOST = ''

class ServerKey():
	def __init__(self):
		#self._private_key = os.urandom(32)
		self._private_key = b'0'*32
		sk = ecdsa.SigningKey.from_string(self._private_key, curve=ecdsa.SECP256k1)
		vk = sk.get_verifying_key()
		self._public_key = vk.to_string()
		self._sign = None

	def generateTypeSign(self, cointype):
		sk = ecdsa.SigningKey.from_string(self._private_key, curve=ecdsa.SECP256k1)
		sign = sk.sign(cointype.encode('UTF-8'))
		self._sign = sign
		return sign

	def verifyTypeSign(self, cointype, typeSign):
		vk = ecdsa.VerifyingKey.from_string(self._public_key, curve=ecdsa.SECP256k1)
		if not vk.verify(typeSign, cointype.encode('UTF-8')):
			return False
		else:
			return True
