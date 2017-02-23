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
				quit();

class outgoing (threading.Thread):
	def __init___(self):
		threading.Thread.__init__(self)
	def run(self):
		while 1:
			data = raw_input()
			data = s.send(data)

print "Login as : "
UN = raw_input()
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("0.0.0.0",8888))
s.send(UN)

pingServer = outgoing()
pingServer.start()
receivePing = incoming()
receivePing.start()