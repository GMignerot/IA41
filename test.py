# Test IA contre IA

import time
from f3base.state import State, Slot
from f3base.ai import minmax, Config


state = State()
players = {Slot.Player1: (Slot.Player2, "joueur 1"), Slot.Player2: (Slot.Player1, "joueur 2")}
currentplayer = Slot.Player1
numtour = 1

print(state)
while state.win()[0] is None:
	opponent, name = players[currentplayer]
	print(f"\nTour {numtour} : {name}")
	print("\n".join([", ".join([str(e.value) for e in s.board]) for s in state.playerhistory]))
	start = time.time()
	action = minmax(state, currentplayer, opponent, Config.AIvAI)
	if action is None:
		break
	state = state.apply(action, currentplayer)
	print(f"Time : {time.time() - start}s")
	print(f"Action : {action}")
	print(state)
	currentplayer = opponent
	numtour += 1

winner, line = state.win()
if winner is not None:
	print(f"Le {players[winner][1]} a gagné en {line}")
else:
	print("Match nul !")
