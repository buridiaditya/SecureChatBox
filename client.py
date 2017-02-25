import socket
import sys
import threading
import math
import random

class cryptoSystem(object):
	def __init__(self,n):
		self.maxv = n
		self.primeSeive = self.seive()
		self.generateKeys()

	def seive(self):
		primeSeive = range(0,self.maxv)
		for i in range(0,self.maxv):
			primeSeive[i] = 0
		for i in range(2,self.maxv):
			j = 2*i
			while(j < self.maxv and primeSeive[j] == 0):
				primeSeive[j] = 1
				j += i
		return primeSeive

	def generateKeys(self):
		blum = []
		count = 0
		i = self.maxv 
		while ( i > 0 and count < 2):
			i -= 1
			if self.primeSeive[i] == 0:
				count += 1
				blum.append(i)
		self.p = blum[0]*2+1
		self.q = blum[1]*2+1
		self.n = self.p*self.q
		publicKey = int(random.random()*math.sqrt(self.maxv))
		v = math.sqrt(publicKey)
		while(v*v != publicKey):
			publicKey = int(random.random()*math.sqrt(self.maxv))
			v = math.sqrt(publicKey)
		self.publicKey = publicKey

	def encrypt(self,message,publicKey,N):
		asciiM = bytearray(message)
		binaryOfChars = []
		encyptedMessage = []
		for i in asciiM:
			binaryOfChars.append(bin(i).split('b')[1])
		for i in binaryOfChars:
			x = random.random()*math.sqrt(N)*10
			temp = []
			for j in i:
				if j == '1':
					temp.append((x*x*publicKey)%N)
				else : 
					temp.append((x*x*publicKey)%N)
			encyptedMessage.append(temp)
		return encyptedMessage


class incoming (threading.Thread):
	def __init___(self):
		threading.Thread.__init__(self)
	def run(self):
		while 1: 
			data = s.recv(1024)
			print data
			if data == "Succesfully Logout Sire!":
				exit();

class outgoing (threading.Thread):
	def __init___(self):
		threading.Thread.__init__(self)
	def run(self):
		while 1:
			data = raw_input()
			data = s.send(data)

def connect(socket,addr):
	try:
		s.connect(addr)
		return "Succesful Connected to " + str(addr[0]) + ":" + str(addr[1])
	except socket.error as msg:
		print msg
		print "Trying to Reconnect to Server " + str(addr[0]) + ":" + str(addr[1])
		return connect(socket,addr)


try:
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error as msg:
	print msg

print connect(s,("0.0.0.0",8888))

print "Login as : "
UN = raw_input()
s.send(UN)

pingServer = outgoing()
pingServer.start()

receivePing = incoming()
receivePing.start()