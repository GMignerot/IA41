import math
import enum
from .state import Slot, State


class Config (enum.Enum):
	PvP = 0
	PvAI = 1
	AIvAI = 2

def finalvalue(state, player, opponent):
	winner, line = state.win()
	if winner is None:
		return 0
	elif winner == player:
		return 10000
	elif winner == opponent:
		return -10000

def value(state, player, opponent, turn):
	winner, line = state.win()
	if winner == player:
		return 10000
	elif winner == opponent:
		return -10000
	else:  # Fonction d'évaluation très arbitraire
		playertokens = 0
		opponenttokens = 0
		emptytokens = 0
		for slot in state.board:
			if slot == player:
				playertokens += 1
			elif slot == opponent:
				opponenttokens += 1
			elif slot == Slot.Square:
				emptytokens += 1
		actioncount = len(state.possibleActions(player))
		return ((playertokens / (opponenttokens + emptytokens)) * 100 - (opponenttokens / (playertokens + emptytokens)) * 100) + actioncount - 2 + 8/turn
		

def maxvalue(state, player, opponent, alpha, beta, horizon, config):
	if state.win()[0] is not None or (state in state.playerhistory and config == Config.AIvAI):
		return finalvalue(state, player, opponent), None
	elif horizon == 0:
		return finalvalue(state, player, opponent), None #, state.branchlength // 2), None
	actions = state.possibleActions(player)
	if len(actions) == 0:
		return finalvalue(state, player, opponent, len(playerpassed)), None
	maxresult = -math.inf
	maxaction = None
	for transition in actions:
		result, _ = minvalue(state.apply(transition, player), player, opponent, alpha, beta, horizon-1, config)
		if result > maxresult:
			maxresult = result
			maxaction = transition
		if maxresult >= beta:
			return maxresult, maxaction
		alpha = max(alpha, maxresult)
	return maxresult, maxaction

def minvalue(state, player, opponent, alpha, beta, horizon, config):
	if state.win()[0] is not None or (state in state.playerhistory and config == Config.AIvAI):
		return -finalvalue(state, opponent, player), None
	elif horizon == 0:
		return -finalvalue(state, opponent, player), None #, state.branchlength // 2), None
	actions = state.possibleActions(opponent)
	if len(actions) == 0:
		return finalvalue(state, player, opponent, len(playerpassed)), None
	minresult = +math.inf
	maxaction = None
	for transition in state.possibleActions(opponent):
		result, _ = maxvalue(state.apply(transition, opponent), player, opponent, alpha, beta, horizon-1, config)
		if result < minresult:
			minresult = result
			minaction = transition
		if minresult <= alpha:
			return minresult, minaction
		beta = min(beta, minresult)
	return minresult, minaction
			

def minmax(state, player, opponent, config, horizon=8):
	v, transition = maxvalue(state, player, opponent, -math.inf, +math.inf, horizon, config)
	return transition
