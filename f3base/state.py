import enum

class Slot (enum.Enum):
	Empty = 0
	Square = 1
	Player1 = 2
	Player2 = 3

class TransitionType (enum.Enum):
	Null = 0
	AddCircle = 1
	PushSquare = 2
	MoveCircle = 3

class Direction (enum.Enum):
	Top = (0, -1)
	Bottom = (0, 1)
	Left = (-1, 0)
	Right = (1, 0)
	
REVERSE_DIRECTION = {Direction.Top: Direction.Bottom, Direction.Bottom: Direction.Top, Direction.Left: Direction.Right, Direction.Right: Direction.Left}

# [0 1 2]
# [3 4 5]
# [6 7 8]

EMPTY_POSITIONS = {
	0: {1: Direction.Right, 2: Direction.Right, 3: Direction.Bottom, 6: Direction.Bottom},
	1: {0: Direction.Left, 2: Direction.Right, 4: Direction.Bottom, 7: Direction.Bottom},
	2: {0: Direction.Left, 1: Direction.Left, 5: Direction.Bottom, 8: Direction.Bottom},
	3: {0: Direction.Top, 4: Direction.Right, 5: Direction.Right, 6: Direction.Bottom},
	4: {1: Direction.Top, 3: Direction.Left, 5: Direction.Right, 7: Direction.Bottom},
	5: {2: Direction.Top, 3: Direction.Left, 4: Direction.Left, 8: Direction.Bottom},
	6: {0: Direction.Top, 3: Direction.Top, 7: Direction.Right, 8: Direction.Right},
	7: {1: Direction.Top, 4: Direction.Top, 6: Direction.Left, 8: Direction.Right},
	8: {2: Direction.Top, 5: Direction.Top, 6: Direction.Left, 7: Direction.Left},
}

PLAYERS = (Slot.Player1, Slot.Player2)


class Transition (object):
	def __init__(self, type, position, value=None):
		self.type = type
		self.position = position
		self.value = value
	
	def __eq__(self, tr):
		if tr is None: return False
		return tr.type == self.type and tr.position == self.position and tr.value == self.value
	
	def __str__(self):
		return f"({self.type}, {self.position}, {self.value})"
	
	def __repr__(self):
		return self.__str__()


class State (object):
	def __init__(self, board=None):
		if board is None:
			self.board = [Slot.Square, Slot.Square, Slot.Square, Slot.Square, Slot.Empty, Slot.Square, Slot.Square, Slot.Square, Slot.Square]
		else:
			self.board = board
		self.actioncache = {Slot.Player1: None, Slot.Player2: None}
		self.origin = None
		self.playerhistory = ()
		self.opponenthistory = ()
		self.originplayer = None
		self.originaction = Transition(TransitionType.Null, 0)
		self.branchlength = 0
		
	def apply(self, transition, player, check=True):
		if check:
			if transition not in self.possibleActions(player):
				raise ValueError(f"Impossible transition {transition}")
		
		newstate = self.copy()
		newstate.origin = self
		newstate.originplayer = player
		newstate.originaction = transition
		newstate.branchlength = self.branchlength + 1
		newstate.playerhistory = self.opponenthistory
		newstate.opponenthistory = self.playerhistory + (self, )
		
		if transition.type == TransitionType.AddCircle:
			newstate.board[transition.position] = player
		elif transition.type == TransitionType.MoveCircle:
			newstate.board[transition.value] = player
			newstate.board[transition.position] = Slot.Square
		elif transition.type == TransitionType.PushSquare:
			emptypos = self.board.index(Slot.Empty)
			if transition.value == Direction.Right:
				if emptypos == transition.position + 2:
					newstate.board[transition.position + 2] = newstate.board[transition.position + 1]
				newstate.board[transition.position + 1] = newstate.board[transition.position]
			elif transition.value == Direction.Left:
				if emptypos == transition.position - 2:
					newstate.board[transition.position - 2] = newstate.board[transition.position - 1]
				newstate.board[transition.position - 1] = newstate.board[transition.position]
			elif transition.value == Direction.Bottom:
				if emptypos == transition.position + 6:
					newstate.board[transition.position + 6] = newstate.board[transition.position + 3]
				newstate.board[transition.position + 3] = newstate.board[transition.position]
			elif transition.value == Direction.Top:
				if emptypos == transition.position - 6:
					newstate.board[transition.position - 6] = newstate.board[transition.position - 3]
				newstate.board[transition.position - 3] = newstate.board[transition.position]
			newstate.board[transition.position] = Slot.Empty
		return newstate
	
	def possibleActions(self, player):
		"""Optimisé mais moche
		Renvoie toutes les transitions valides à partir de l’état. Le résultat est mis en cache."""
		if self.actioncache[player] is not None:
			return self.actioncache[player]
		else:
			moglichkeiten = []
			playercircles = 0
			squares = []
			for i, value in enumerate(self.board):
				if value == Slot.Square:
					squares.append(i)
				elif value == player:
					playercircles += 1
			
			emptypos = self.board.index(Slot.Empty)
			for position, value in enumerate(self.board):
				# AddCircle
				if value == Slot.Square and playercircles < 3:
					moglichkeiten.append(Transition(TransitionType.AddCircle, position))
					
				# MoveCircle
				if value == player:  # Gaffe, le sujet est pas clair : c’est que un pion du joueur en cours
					for destination in squares:
						moglichkeiten.append(Transition(TransitionType.MoveCircle, position, destination))
							
				# PushSquare
				if emptypos in EMPTY_POSITIONS[position]:
					transition = Transition(TransitionType.PushSquare, position, EMPTY_POSITIONS[position][emptypos])
					if self.originaction.type == TransitionType.PushSquare:
						if transition.value.value[0] == -self.originaction.value.value[0] and transition.value.value[1] == -self.originaction.value.value[1]:
							if self.origin != self.apply(transition, player, False):
								moglichkeiten.append(transition)
						else:
							moglichkeiten.append(transition)
					else:
						moglichkeiten.append(transition)
			
			self.actioncache[player] = moglichkeiten
			return moglichkeiten
	
	def win(self):
		"""Si une configuration gagnante est trouvée, retourne le gagnant et les cases de l’alignement. Sinon, renvoie None"""
		for i in range(3):
			if self.board[i] == self.board[i + 3] == self.board[i + 6] and self.board[i] in PLAYERS:  # colonne
				return self.board[i], (i, i+3, i+6)
			if self.board[i*3] == self.board[i*3 + 1] == self.board[i*3 + 2] and self.board[i*3] in PLAYERS:  # ligne
				return self.board[i*3], (i*3, i*3+1, i*3+2)
		# Diagonales
		if self.board[0] == self.board[4] == self.board[8] and self.board[0] in PLAYERS:
			return self.board[0], (0, 4, 8)
		if self.board[2] == self.board[4] == self.board[6] and self.board[2] in PLAYERS:
			return self.board[2], (2, 4, 6)
		return None, None
	
	def copy(self):
		newstate = State(self.board.copy())
		return newstate
	
	def __eq__(self, state):
		if state is None: return False
		return self.board == state.board
	
	def __str__(self):
		board = [slot.value for slot in self.board]
		return f"{board[0:3]}\n{board[3:6]}\n{board[6:9]}"
	
	def __repr__(self):
		return f"State({self.board})"
		
	def _possibleActions_understandable(self, player):
		"""Lisible et avec bon algo pour les possibilités plutôt qu’un tableau opti mais moche"""
		moglichkeiten = []
		
		# AddCircle
		for position, value in enumerate(self.board):
			if value == Slot.Square:
				moglichkeiten.append(Transition(TransitionType.AddCircle, position))
		
		# MoveCircle
		for position, value in enumerate(self.board):
			if value == player:  # Gaffe, le sujet est pas clair : c’est que un pion du joueur en cours
				for destination, value in enumerate(self.board):
					if value == Slot.Square:
						moglichkeiten.append(Transition(TransitionType.MoveCircle, position, destination))
		
		# PushSquare
		emptypos = self.board.index(Slot.Empty)
		emptyrow = emptypos % 3
		emptycol = emptypos // 3
		for position, value in enumerate(self.board):
			row = position % 3
			col = position // 3
			if value != Slot.Empty and (emptyrow == row or emptycol == col):
				if col != 0:
					moglichkeiten.append(Transition(TransitionType.PushSquare, position, Direction.Left))
				if col != 2:
					moglichkeiten.append(Transition(TransitionType.PushSquare, position, Direction.Right))
				if row != 0:
					moglichkeiten.append(Transition(TransitionType.PushSquare, position, Direction.Top))
				if row != 2:
					moglichkeiten.append(Transition(TransitionType.PushSquare, position, Direction.Bottom))
				


"""import timeit, random

def testopti():
	state = State()
	emptypos = random.randint(0, 9)
	board = random.choices(list(Slot), k=8)
	board.insert(emptypos, Slot.Empty)
	state.board = board
	state.possibleActions(Slot.Player1)

def testnul():
	state = State()
	emptypos = random.randint(0, 9)
	board = random.choices(list(Slot), k=8)
	board.insert(emptypos, Slot.Empty)
	state.board = board
	state._possibleActions_understandable(Slot.Player1)

print("Opti : ", timeit.timeit("testopti()", number=500000, setup="from __main__ import testopti"))
print("Nul  : ", timeit.timeit("testnul()", number=500000, setup="from __main__ import testnul"))
"""
if __name__ == "__main__":
	import pprint, random
	state = State()
	pprint.pprint(state.possibleActions(Slot.Player1))
	transition = random.choice(state.possibleActions(Slot.Player1))
	print(transition)
	newstate = state.apply(transition, Slot.Player1)
	print(newstate)
	
