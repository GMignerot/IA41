import math
from .state import Slot, State


def value(state, player, opponent, turn):
	winner, line = state.win()
	if winner is None:
		return 0
	elif winner == player:
		return 100*turn
	elif winner == opponent:
		return -100*turn

def maxvalue(state, player, opponent, playerpassed, opponentpassed, alpha, beta, horizon):
	if state.win()[0] is not None or state in playerpassed or horizon == 0:
		return value(state, player, opponent, len(playerpassed)), None
	actions = state.possibleActions(player)
	#print(f"Max : {len(actions)}")
	if len(actions) == 0:
		return value(state, player, opponent, len(playerpassed)), None
	playerpassed += (state, )
	#print(f"\r{len(playerpassed)}, {len(opponentpassed)}, {len(actions)}   ", end="")
	maxresult = -math.inf
	maxaction = None
	for transition in actions:
		result, _ = minvalue(state.apply(transition, player), player, opponent, playerpassed, opponentpassed, alpha, beta, horizon-1)
		if result > maxresult:
			maxresult = result
			maxaction = transition
		if maxresult >= beta:
			return maxresult, maxaction
		alpha = max(alpha, maxresult)
	return maxresult, maxaction

def minvalue(state, player, opponent, playerpassed, opponentpassed, alpha, beta, horizon):
	if state.win()[0] is not None or state in opponentpassed or horizon == 0:
		return value(state, player, opponent, len(playerpassed)), None
	actions = state.possibleActions(opponent)
	#print(f"Min : {len(actions)}")
	if len(actions) == 0:
		return value(state, player, opponent, len(playerpassed)), None
	opponentpassed += (state, )
	#print(f"\r{len(playerpassed)}, {len(opponentpassed)}, {len(actions)}   ", end="")
	minresult = +math.inf
	maxaction = None
	for transition in state.possibleActions(opponent):
		result, _ = maxvalue(state.apply(transition, opponent), player, opponent, playerpassed, opponentpassed, alpha, beta, horizon-1)
		if result < minresult:
			minresult = result
			minaction = transition
		if minresult <= alpha:
			return minresult, minaction
		beta = min(beta, minresult)
	return minresult, minaction
			

def minmax(state, player, opponent, horizon=8):
	if state.win()[0] is not None: return None
	print("")
	v, transition = maxvalue(state, player, opponent, (), (), -math.inf, +math.inf, horizon)
	return transition