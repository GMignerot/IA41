# Test IA contre IA

from f3base.state import State, Slot
from f3base.ai import minmax


state = State()
players = {Slot.Player1: (Slot.Player2, "joueur 1"), Slot.Player2: (Slot.Player1, "joueur 2")}
currentplayer = Slot.Player1
numtour = 1

print(state)
while state.win()[0] is None:
	opponent, name = players[currentplayer]
	print(f"Tour {numtour} : {name}")
	action = minmax(state, currentplayer, opponent)
	state = state.apply(action, currentplayer)
	print(action)
	print(state)
	currentplayer = opponent
	numtour += 1

winner, line = state.win()
print(f"Le {players[winner][1]} a gagné en {line}")