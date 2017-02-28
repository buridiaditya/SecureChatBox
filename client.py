import socket
import sys
import threading
import math
import random
import binascii 
from fractions import gcd

class cryptoSystem(object):
	def __init__(self,n):
		self.maxv = n
		self.primeSeive = self.seive()
		self.generateKeys()
		
	def seive(self):
		primeSeive = range(0,self.maxv)
		for i in range(0,self.maxv):
			primeSeive[i] = 0

		primeSeive[0] = 1
		primeSeive[1] = 1

		for i in range(2,self.maxv):
			if primeSeive[i] == 0:
				j = 2*i
				while(j < self.maxv):
					primeSeive[j] = 1
					j += i
		return primeSeive

	def modularExponentiation(self,a,p,N):
		if p == 0:
			return 1
		v = self.modularExponentiation(a,p/2,N)
		if p%2 == 0:
			e = (v*v)%N
		else :
			e = (((v*v)%N) * a) % N
		return e

	def generateKeys(self):
		blum = []
		count = 0
		i = int(self.maxv / 2 - 1)
		p = 4
		q = 4
		self.p = 4
		self.q = 4

 		while (self.primeSeive[self.p] == 1 or self.primeSeive[p] == 1):
			p = int(random.random()*i)
			self.p = p*2 + 1
			
		while (self.primeSeive[self.q] == 1 or self.primeSeive[q] == 1):
			q = int(random.random()*i)
			self.q = q*2 + 1

		self.n = self.p * self.q
		self.publicKey = self.n-1

	def encrypt(self,message,publicKey,N):
		asciiM = bytearray(message,"UTF-8")
		binaryOfChars = []
		cipher = "" 
		for i in asciiM:
			binaryOfChars.append( bin(i).split('b')[1] )
		for i in binaryOfChars:
			for j in i:
				x = int( ( random.random() ) * N)
				while(gcd(x,N) != 1):
					x = int( ( random.random() ) * N)
				if j == '1':
					c = ( ( (x*x) % N ) * publicKey) % N 
				else : 
					c = (x*x)%N
				cipher += str(c)+" "
			cipher = cipher[0:len(cipher)-1]
			cipher += ":"
		cipher = cipher[0:len(cipher)-1]
		return cipher

	def decrypt(self,cipher):
		message = ""
		M = cipher.split(':')
		for j in M:
			binString = ""
			for i in j.split(' '):
				k = int(i)
				v = self.modularExponentiation(k,(self.p-1)/2,self.p)
				if v == 1:
					binString += "0"
				else:
					binString += "1"
			message += chr(int(binString,2))
		return message

class incoming (threading.Thread):
	def __init___(self):
		threading.Thread.__init__(self)
	def run(self):
		while 1: 
			data = s.recv(4096)
			comm = data.split(":",1)
			if comm[0] == "keys":	
				keys = comm[1].split(":")
				cipher =  c.encrypt(message,int(keys[0]),int(keys[1]))
				s.send(cipher) 
			elif len(comm) == 1:
				print data
				if data == "Succesfully Logout Sire!":
					exit();
			else :
				print comm[0] + " > "+ c.decrypt(comm[1])
			

class outgoing (threading.Thread):
	def __init___(self):
		threading.Thread.__init__(self)
	def run(self):
		while 1:
			data = raw_input()
			M = data.split(":",1)
			if len(M) != 2:
				print "Invalid Input"
				continue
			global message 
			message = M[1].strip()
			user = M[0].lower().strip()
			s.send(user)
			if user == "server":
				s.send(message)
			
def connect(socket,addr):
	try:
		s.connect(addr)
		return "Succesful Connected to " + str(addr[0]) + ":" + str(addr[1])
	except socket.error as msg:
		print msg
		print "Trying to Reconnect to Server " + str(addr[0]) + ":" + str(addr[1])
		return connect(socket,addr)

message = ""
user = ""

c = cryptoSystem(100000)
try:
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error as msg:
	print msg

print connect(s,("127.0.0.1",8888))

print "Login as : "
UN = raw_input()
s.send(UN+":"+str(c.publicKey)+":"+str(c.n))
print s.recv(1024)
pingServer = outgoing()
pingServer.start()

receivePing = incoming()
receivePing.start()

# csa = c.encrypt("buridi",c.publicKey,c.n)
# print c.decrypt(csa)