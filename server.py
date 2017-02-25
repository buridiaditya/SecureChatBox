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
			command = self.soc.recv(1024)	
			data = command.split(":",1)
			if len(data) != 1:
				message = data[1].strip()
				user = data[0].lower().strip()
				if user == 'server':
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
							i[1].send(self.name + ">: " + message)
			else : 
				self.soc.send("Invalid Command")

clients = []
HOST = '0.0.0.0'
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
		name = conn.recv(1024)
		conn.send("Welcome to NoseBook!")
		clie = client(conn,addr,name)
		clients.append([name,conn])
		clie.start()
except KeyboardInterrupt:
	s.close()
	sys.exit()
except socket.error as msg:
	print msg