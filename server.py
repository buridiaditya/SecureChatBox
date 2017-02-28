import socket
import sys
import threading
import re

class client (threading.Thread):
	def __init__(self,clientSocket,clientAddr,name):
		threading.Thread.__init__(self)
		self.soc = clientSocket
		self.addr = clientAddr
		self.name = name
	def run(self):
		while 1:
			user = self.soc.recv(4096)
			if user != "server":
				for i in clients:
					if i[0].lower() == user:
						self.soc.send("keys:"+str(i[2])+":"+str(i[3]))
			message = self.soc.recv(4096)	
			if user == "server":
				if message == "logout":
					self.soc.send("Succesfully Logout Sire!")
					return
				elif message == "show friends":
					for i in clients:
						if i[0] != self.name:
							self.soc.send(i[0])
			else:
				for i in clients:
					if i[0].lower() == user:
						i[1].send(self.name + ":" + message)
	
clients = []
HOST = '127.0.0.1'
PORT = 8888
addr = (HOST,PORT)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
	s.bind(addr)
	print "Socket in Listening"
	s.listen(10)
	while 1:
		conn,addr = s.accept()
		print "Connected to " + str(addr[0]) + " : " + str(addr[1])
		inc = conn.recv(1024)
		data = inc.split(":")
		conn.send("Welcome to NoseBook!")
		clie = client(conn,addr,data[0])
		clients.append([data[0],conn,int(data[1]),int(data[2])])
		clie.start()
except KeyboardInterrupt:
	s.close()
	sys.exit()
except socket.error as msg:
	print msg