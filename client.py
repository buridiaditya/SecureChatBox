import socket
import sys
import threading

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