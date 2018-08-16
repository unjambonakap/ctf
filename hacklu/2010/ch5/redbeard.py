from battleships import *
import SocketServer
import time
import socket
import threading
import sys

SECRET_PW = "notset"

class NetworkPlayer(IOPlayer):

	def __init__(self, server):
		self.server = server
		name = self.promptUser("Btw, what was your name pirate?")
		IOPlayer.__init__(self, name)
				
	def printMsgLine(self, msg):
		self.server.request.send(msg + "\r\n")
		
	def printMsg(self, msg):
		self.server.request.send(msg)
	
	def promptUser(self, msg):

		self.printMsgLine(msg)
		self.printMsg(">>> ")
		
		input = self.server.request.recv(1024).strip()
		
		i = 0
		while ((not input) and (i<5)):
			input = self.server.request.recv(1024).strip()
			i += 1
			
		return input 
		
		
class CaptainRedbeard(Player):

	msgSuccess = ["Hahaha, is this your first sea-fight?!", "HrhrhrhrHrrrrrr!", "*Sing* 13 men on the dead man's chest, and a buddle of rum...","W0000ty!","rofl","You callin you'self mighty pirate? Hohohoho...","Still want your 500P?!","You better sail home while you can!"]
	msgFail = ["GrrrrrRrrrRrr.","Must be the wind...","Uhm.","o_O","O_o","What-the...?!","Hahaha - this means nothing!","A lucky man you are.",":x","This can't be...","GrrrRrrrrRrrrrrrrrrrrrrrrrrrrrrrr.","There must be something wrong with me cannons."]

	#hitRatio example: (1,3) means: "one in three shots is a hit"
	def __init__(self, hitRatio, opponent, server):
		self.server = server
		self.opponent = opponent
		self.counter = 0
		self.hitRatio = hitRatio
		Player.__init__(self,"Cap'n Redbeard")
		self.printMsgLine("Hrhrhr, these 500P are mine. I'll send all yo ships down to the fish.")
		
	def shoot(self):
		#think...
		time.sleep(2)
		#yeah, shoot some stuff!
		if (self.counter % self.hitRatio[1]) < self.hitRatio[0]:
			for ship in self.opponent.board.ships:
				if ship.alive:
					for field in ship.fields:
						if field.hit == False:
							self.counter += 1
							return field
							
		#shoot somewhere
		else:
			self.counter += 1
			return Point(self.randInt(0, self.board.size-1),self.randInt(0, self.board.size-1))
								
	def notify(self, b, shot, result):
		if BOARD["own"] == b:
			if EVENT["missed"] == result:
				self.printMsgLine(self.msgSuccess[self.randInt(0,len(self.msgSuccess)-1)])
			else:
				self.printMsgLine(self.msgFail[self.randInt(0,len(self.msgFail)-1)])
		
		else:
			if EVENT["missed"] == result:
				self.printMsgLine(self.msgFail[self.randInt(0,len(self.msgFail)-1)])
			elif EVENT["hit"] == result:
				self.printMsgLine(self.msgSuccess[self.randInt(0,len(self.msgSuccess)-1)])
			else:
				_msg = "Got one! "
				_msg += self.msgSuccess[self.randInt(0,len(self.msgSuccess)-1)]
				self.printMsgLine(_msg)

		return
		
	def createBoard (self, boardSize, shipSizes):
		self._createBoardRandom(boardSize, shipSizes)
		
	def printMsgLine(self, msg):
	#	self.server.request.send("" + self.name + "> " + msg + "\r\n")
		print "...<<";
		
	def setHitRatio(self, hitRatio):
		self.hitRatio = hitRatio
		self.counter = 0
				
class GameSession(SocketServer.BaseRequestHandler):

	def handle(self):

		# Greeting
		print "Got connection."
		
		self.printPlotStart()
		
		p1 = NetworkPlayer(self)				
		rb = CaptainRedbeard((3,5),p1,self)
		
		time.sleep(2)
		
		self.request.send("Looks like yo got no choice, huh?\r\n")
		
		game = Game(10, [4,3,3,2,1,1],p1,rb)
		if (game.play() == 0):
			self.request.send("Yeah, you won! But what it this? Reinforcements for both sides!\r\n")
			time.sleep(2)
		else:
			self.request.send("You lost!\r\n")
			time.sleep(2)
			return
		
		#redbeard's getting angry
		rb.setHitRatio((4,5))
		
		game = Game(10, [4,3,3,2,1,1],p1,rb)
		if (game.play() == 0):
			self.request.send("Yeah, you won! But what it this? Reinforcements for both sides!\r\n")
			time.sleep(2)
		else:
			self.request.send("You lost!\r\n")
			time.sleep(2)
			return
			
		#redbeard's getting really angry
		rb.setHitRatio((5,5))
		
		game = Game(10, [4,3,3,2,1,1],p1,rb)
		if (game.play() == 0):
			self.request.send("Yeah, you won the 3rd time! Redbeard is backing off, look!\r\nHere are your 500P: ")
			self.request.send(SECRET_PW)
			time.sleep(60)
		else:
			self.request.send("You lost!\r\n")
			time.sleep(2)
			return
			
	def printPlotStart(self):
		self.request.send("So you heard from an almost reliable source, that there are some easy 500P to pirate just 'round the corner.\r\n")
		self.request.send("Of course yo and yo always P-hungry crew set sail immediately!\r\n")
		time.sleep(2)
		self.request.send(plot0)
		time.sleep(2)
		self.request.send("But all of a sudden...\r\n")
		time.sleep(2)
		self.request.send("THE FEARSOME CAPTAIN REDBEARD AND HIS ARMADA OF GHOST SHIPS ALL STUFFED WITH UNDEAD PIRATES APPEARS!!!\r\n")
		time.sleep(2)
		self.request.send("crap...\r\n")
		time.sleep(2)
		
		
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	
    pass
		
			
if __name__ == "__main__":

	
	#read-in plot files
	f = file("plot0.txt","rb")
	plot0 = f.read()
	f.close()
	###################
	
	#read-in secret pw
	f = file("pw.txt","rb")
	SECRET_PW = f.read()
	f.close()
	###################
	
	HOST, PORT = "", 2204
	
	server = ThreadedTCPServer((HOST, PORT), GameSession)
	server.timeout = None #explicitly set no timeout
	ip, port = server.server_address

	# Start a thread with the server -- that thread will then start one
	# more thread for each request
	server_thread = threading.Thread(target=server.serve_forever)

	server_thread.setDaemon(True)
	server_thread.start()
	print "Server loop running in thread:", server_thread.getName()
	
	server.serve_forever()
		
