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
			if command == "Logout Jarvis":
				self.soc.send("Succesfully Logout Sire!")
				return
			elif command == "Show Friends" or command == "show friends" or command == "Show friends":
				for i in clients:
					if i[0] != self.name:
						self.soc.send(i[0])
			else :
				data = re.split(":",command)
				message = data[1]
				user = data[0]
				for i in clients:
					if i[0] == user:
						i[1].send(self.name + ": " +message)

clients = []
HOST = '0.0.0.0'
PORT = 8888
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
addr = (HOST,PORT)
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
s.close()