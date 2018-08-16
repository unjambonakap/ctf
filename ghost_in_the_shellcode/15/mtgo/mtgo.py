import socket
import datetime
import random

basedeck = [
	"Birds of Paradise1",
	"Birds of Paradise2",
	"Birds of Paradise3",
	"Birds of Paradise4",
	"Eternal Witness1",
	"Kitchen Finks1",
	"Kitchen Finks2",
	"Kitchen Finks3",
	"Linvala, Keeper of Silence1",
	"Murderous Redcap1",
	"Noble Hierarch1",
	"Noble Hierarch2",
	"Orzhov Pontiff1",
	"Reclamation Sage1",
	"Restoration Angel1",
	"Restoration Angel2",
	"Reveillark1",
	"Scavenging Ooze1",
	"Shriekmaw1",
	"Siege Rhino1",
	"Siege Rhino2",
	"Sin Collector1",
	"Spellskite1",
	"Voice of Resurgence1",
	"Voice of Resurgence2",
	"Voice of Resurgence1",
	"Wall of Roots1",
	"Wall of Roots2",
	"Abrupt Decay1",
	"Abrupt Decay2",
	"Abrupt Decay1",
	"Birthing Pod1",
	"Birthing Pod2",
	"Birthing Pod1",
	"Birthing Pod2",
	"Thoughtseize1",
	"Thoughtseize2",
	"Forest1",
	"Forest2",
	"Forest3",
	"Gavony Township1",
	"Gavony Township2",
	"Godless Shrine1",
	"Marsh Flats1",
	"Overgrown Tomb1",
	"Overgrown Tomb2",
	"Plains1",
	"Razorverge Thicket1",
	"Razorverge Thicket2",
	"Razorverge Thicket1",
	"Swamp1",
	"Temple Garden1",
	"Verdant Catacombs1",
	"Verdant Catacombs2",
	"Verdant Catacombs1",
	"Verdant Catacombs2",
	"Windswept Heath1",
	"Windswept Heath2",
	"Windswept Heath3",
	"Windswept Heath4",
]

class sock:
	def sendall(self, data):
		print data
	def recv(self,l):
		return raw_input()

def shuffle(deck):
	for i in xrange(len(deck)):
		s = random.randint(0, len(deck)-1)
		t = deck[s]
		deck[s] = deck[i]
		deck[i] = t

	return deck
def get_tick():
	# gives you a string down to the millisecond*10
	return datetime.datetime.now().isoformat()[:-4]

def game(sock):
	random.seed(get_tick())
	deck = shuffle(basedeck)
	sock.sendall(deck[:7])
	if sock.recv(2048) == ','.join(deck[7:20]):
		return True
	return False

s = sock()
count = 0
cont = True
while count<20 and cont:
	cont = game(s)
	count += 1

if count == 20:
	s.sendall("Huh. Guess this is broken.")
	s.sendall(open('key').read())
else:
	s.sendall("try harder")
