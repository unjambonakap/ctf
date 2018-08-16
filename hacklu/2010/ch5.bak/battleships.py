#classes representing a battleships 
import random
import os
# 0 -> x
# |
# v
# y
#
DEBUG = False

ORIENTATION = {"north":0,"east":1,"south":2,"west":3}
BOARD = {"own":0,"opponents":1}
EVENT = {"missed":0,"hit":1,"sunk":2}

class Point:
		
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Field(Point):
	
	def __init__(self, board, x, y):
		self.board = board
		self.hit = False
		self.ship = None
		
		Point.__init__(self,x,y)
	
	def setShip(self, ship):
		self.ship = ship
		
	def getShip(self):
		return self.ship
	
class ErrorCantPlaceShip(Exception):

	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		
class ErrorNotImplemented(Exception):

	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		
class ErrorCantSetupBoard(Exception):

	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		
		
class Ship:
		
	def __init__(self, board, start, size, orientation):
	
		self.fields = []
		self.board = board
		self.size = size
		self.alive = True
		
		if orientation not in range(len(ORIENTATION)):
			raise ErrorCantPlaceShip("wrong argument")
			return
		
		#check start coords
		if ((start.x < 0) or (start.x > (board.size-1)) or ((start.y < 0) or (start.y > (board.size-1)))):
			raise ErrorCantPlaceShip("start out of bounds")
		
		if orientation == ORIENTATION["north"]: 
			if ((start.y - (size-1)) < 0):
				raise ErrorCantPlaceShip("end out of bounds")
			
			#check if all fields are free
			for y in range(start.y - (size-1), start.y+1):
				field = board.fields[start.x][y] 
				if field.ship != None:
					raise ErrorCantPlaceShip("field already taken")
			
			#copy fields
			for y in range(start.y - (size-1), start.y+1):
				field = board.fields[start.x][y] 
				field.ship = self
				self.fields.append(field)
			
			
		elif orientation == ORIENTATION["east"]:
			if (start.x + (size-1)) > board.size-1:
				raise ErrorCantPlaceShip("end out of bounds")
			
			#check if all fields are free
			for x in range(start.x, start.x+(size-1)+1):
				field = board.fields[x][start.y]	
				if field.ship != None:
					raise ErrorCantPlaceShip("field already taken")
					
			#copy fields			
			for x in range(start.x, start.x+(size-1)+1):
				field = board.fields[x][start.y]	
				field.ship = self
				self.fields.append(field)
			
			
		elif orientation == ORIENTATION["south"]:
			if ((start.y + (size-1)) > board.size-1):
				raise ErrorCantPlaceShip("end out of bounds")
			
			#check if all fields are free
			for y in range(start.y, start.y+(size-1)+1):
				field = board.fields[start.x][y]
				if field.ship != None:
					raise ErrorCantPlaceShip("field already taken")
			
			#copy fields			
			for y in range(start.y, start.y+(size-1)+1):
				field = board.fields[start.x][y]
				field.ship = self
				self.fields.append(field)
			
		elif orientation == ORIENTATION["west"]: 
			if (start.x - (size-1)) < 0:
				raise ErrorCantPlaceShip("end out of bounds")
			
			#check if all fields are free
			for x in range(start.x - (size-1), start.x+1):
				field = board.fields[x][start.y]
				if field.ship != None:
					raise ErrorCantPlaceShip("field already taken")
					
			#copy fields			
			for x in range(start.x - (size-1), start.x+1):
				field = board.fields[x][start.y]
				field.ship = self
				self.fields.append(field)
				
				
	def updateStatus(self):
		#check if still alive
		dead = True
		for field in self.fields:
			dead = dead and field.hit
			
		self.alive = not dead
			
		
class Board:
	
	def __init__(self, size):
		#create a square board
		self.size = size
		self.fields = []
		
		for i in range(size):
			column = []
			for j in range(size):
				column.append(Field(self,i,j))
				
			self.fields.append(column)
			
	
class UnknownBoard(Board):
	
	def __str__(self):
		viz = " |"
		for i in range(self.size):
			viz += str(i) + " "
		viz += "\r\n"
		viz += "-"*(2*self.size+1)
		viz += "\r\n"
		
		i = 0	
		for row in range(self.size):
			viz += str(i) + "|"
			for column in range(self.size):
				field = self.fields[column][row]
				
				if field.hit: #hit
					if field.ship == True:
						viz += "S" #ship
					else:
						viz += "X" #no ship
						
				else: #no hit
					viz += "?"
				viz += " "
			
			i+=1
			viz += "\r\n"
		return viz 
		
	def shot(self, shot, success):
	
		field = self.fields[shot.x][shot.y]
		
		field.hit = True
		field.ship = success

		
class GameBoard(Board):

	def __init__(self, size):
		self.ships = []
		Board.__init__(self, size)

	def __str__(self):
		viz = " |"
		for i in range(self.size):
			viz += str(i) + " "
		viz += "\r\n"
		viz += "-"*(2*self.size+1)
		viz += "\r\n"
		
		i = 0
		for row in range(self.size):
			viz += str(i) + "|"
			for column in range(self.size):
				field = self.fields[column][row]
				
				if field.hit: #hit
					if field.ship != None:
						viz += "S" #ship
					else:
						viz += "X" #no ship
						
				else: #no hit
					if field.ship != None:
						viz += "s" #ship
					else:
						viz += "O" #no ship
				viz += " "
				
			viz += "\r\n"
			i += 1
			
		return viz
	
	def addShip(self, start, size, orientation):
		
		ship = Ship(self, start, size, orientation)
		self.ships.append(ship)
		
	def hit(self, shot):
	
		field = self.fields[shot.x][shot.y]
		
		if (field.ship != None) and not field.hit:
			
			field.hit = True
			field.ship.updateStatus()
			
			if field.ship.alive == False:
				result = EVENT["sunk"]
			else:
				result = EVENT["hit"]
				
		else:
			field.hit = True
			result = EVENT["missed"]
	
		return result
	
	def lost(self):
		#check if the player of this board has lost
		alive = False
		for ship in self.ships:
			alive = alive or ship.alive
			
		return not alive
	
		
class Player:
	
	def __init__(self, name):
		self.name = name
		
		#init Wichmann-Hill prng with 256 bits (32*8) seed
		self.rand = random.WichmannHill(os.urandom(32))
		
	def shoot(self):
		raise ErrorNotImplemented("called pure virtual method shoot()")
		return
		
	def notify(self, msg, shot, result):
		raise ErrorNotImplemented("called pure virtual method notify()")
		return
		
	def randInt(self, low, high):
		r = self.rand.randint(low,high)
		return r
		
	def createBoard (self, boardSize, shipSizes):
		raise ErrorNotImplemented("called pure virtual method notify()")
		return
		
	def _createBoardRandom(self, boardSize, shipSizes):
		
		self.board = GameBoard(boardSize)
		
		#place ships on board
		for shipSize in shipSizes:
			if DEBUG:
				print "\tPlacing ship of size %d." % shipSize
				
			placed = False
			oi = self.randInt(0, len(ORIENTATION)-1) #initial orientation of ship
			#set starting point of ship randomly
			start = Point(self.randInt(0, boardSize-1),self.randInt(0, boardSize-1))
			xOffset = 0
			yOffset = 0
			#try till it fits :)
			while (placed == False):
				orientation = 0
				
				#increase offsets until ship can be placed
				start.x = (start.x + xOffset) % boardSize
				start.y = (start.y + yOffset) % boardSize
								
				if DEBUG:
					print "\t\tTrying x=%d, y=%d." % (start.x, start.y)
				
				#try all four orientations before increasing the offsets
				while (orientation < len(ORIENTATION)) and (placed == False):
					if DEBUG:
						print "\t\tOrientation: %d" % (orientation + oi)
					try:
						self.board.addShip(start, shipSize, (orientation + oi) % len(ORIENTATION))
						placed = True
						if DEBUG:
							print self.board
					except ErrorCantPlaceShip, exception:
						if DEBUG:
							print exception
							
						orientation += 1
						
				xOffset += 1
				if (xOffset % boardSize) == 0:
					yOffset +=1
					if yOffset == boardSize:
					#this should never happen
						raise ErrorCantSetupBoard("argh.")
						
						
class IOPlayer(Player):

	def printMsgLine(self, msg):
		raise ErrorNotImplemented("called pure virtual method printMsgLine()")
		return
		
	def printMsg(self, msg):
		raise ErrorNotImplemented("called pure virtual method printMsg()")
		return
		
	def promptUser(self, msg):
		raise ErrorNotImplemented("called pure virtual method promptUser()")
		return
	
	def shoot(self):
		
		while (True):
			input = self.promptUser("[>] %s it's your turn - where to shoot?" % self.name).split()
			
			if not input:
				self.printMsgLine("[i] No input, try again.")
				
			elif len(input) != 2:
				self.printMsgLine("[i] Input is not of format [digit digit], try again.")
				
			elif input[0].isdigit() == False or input[1].isdigit() == False:
				self.printMsgLine("[i] Input is of wrong format, try again.")
				
			else:
				p = Point(int(input[0],10), int(input[1],10))
				if p.x in range(self.board.size) and p.y in range(self.board.size):
					return p
				else:
					self.printMsgLine("[i] Input is out of bounds, try again.")
					
					
	def notify(self, b, shot, result):
	
		if b == BOARD["own"]:
			msg = "\r\n[i] Your opponent"
		else:
			msg = "\r\n[i] You"
		
		#result msg
		if result == EVENT["missed"]:
			msg += " missed while shooting at [%d,%d]." % (shot.x, shot.y)
		elif result == EVENT["hit"]:
			msg += " hit a ship while shooting at [%d,%d]." % (shot.x, shot.y)
		else:
			msg += " sunk a ship while shooting at [%d,%d]." % (shot.x, shot.y)
			
		self.printMsgLine(msg)
		
		#board views
		if b == BOARD["own"]:
			#print own board
			self.printMsgLine("[i] Your board was updated:")
			self.printMsg(str(self.board))
			self.printMsgLine("")
			
		else:
			self.printMsgLine("[i] Your view of your opponent's board:")
			self.oppBoard.shot(shot, (result != EVENT["missed"]))
			
			#print view of opp's board
			self.printMsg(str(self.oppBoard))
			self.printMsgLine("")
		
	def createBoard (self, boardSize, shipSizes):
		#create shadow board for opponent
		self.oppBoard = UnknownBoard(boardSize)
		self._createBoardRandom(boardSize, shipSizes)
		self.printMsgLine("[i] Your ships are positioned like this:")
		self.printMsg(str(self.board))

#example for IOPlayer
class ConsolePlayer(IOPlayer):

	def promptUser(self, msg):
		return raw_input(msg)
		
	def printMsgLine(self, msg):
		print msg
		
	def printMsg(self, msg):
		print msg
			
class Game:
	
	def __init__(self, boardSize, shipSizes, p1, p2):
		self.p1 = p1
		self.p2 = p2
		
		p1.createBoard(boardSize, shipSizes)
		p2.createBoard(boardSize, shipSizes)
		
	def play(self):
		#p1 starts, nintendo style ;)
		players = [self.p1,self.p2]
		active = 0
		while(True):
			passive = (active+1) % 2
			
			shot = players[active].shoot()
			result = players[passive].board.hit(shot)
			
			players[passive].notify(BOARD["own"],shot, result)
			players[active].notify(BOARD["opponents"],shot, result)
			
			
			if (players[passive].board.lost() == True):
				return active
			
			if result==EVENT["missed"]:
				#no hit? next player's turn!
				active = passive
			