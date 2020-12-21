import random
from Player import*
from os import system, name

class Game:

	def __init__(self):
		self.state = [1,1,1,1,0,1,1,1,1]

	def reset(self):
		self.state = [0,1,1,1,1,1,1,1,1] 
		
	def display(self):

		
		a = self.convertSymbols(self.state[0])
		b = self.convertSymbols(self.state[1])
		c = self.convertSymbols(self.state[2])
		d = self.convertSymbols(self.state[3])
		e = self.convertSymbols(self.state[4])
		f = self.convertSymbols(self.state[5])
		g = self.convertSymbols(self.state[6])
		h = self.convertSymbols(self.state[7])
		i = self.convertSymbols(self.state[8])

		""" 
		│ ┤ ├ ┴ ┬ ┼ ─ └ ┐ ┘ ┌
		
		Virgil : ['carre','carre','carre','pionJ2','carre','','pionJ1','carre','carre']

		┌─────────┬─────────┬─────────┐
		│  ┌───┐  │  ┌───┐  │  ┌───┐  │ 
		│  │ a │  │	 │ b │  │  │ c │  │
		│  └───┘  │  └───┘  │  └───┘  │
		├─────────┼─────────┼─────────┤
		│  ┌───┐  │  ┌───┐  │  ┌───┐  │ 
		│  │ d │  │	 │ e │  │  │ f │  │
		│  └───┘  │  └───┘  │  └───┘  │
		├─────────┼─────────┼─────────┤
		│  ┌───┐  │  ┌───┐  │  ┌───┐  │ 
		│  │ g │  │	 │ h │  │  │ i │  │
		│  └───┘  │  └───┘  │  └───┘  │
		└─────────┴─────────┴─────────┘
		"""

		print("\n\n"
			  "┌─────────┬─────────┬─────────┐\n"
			  "│0 ┌───┐  │1 ┌───┐  │2 ┌───┐  │\n"
			       +a        +b        +c+  "│\n"
			  "│  └───┘  │  └───┘  │  └───┘  │\n"
			  "├─────────┼─────────┼─────────┤\n"
			  "│3 ┌───┐  │4 ┌───┐  │5 ┌───┐  │\n"
			       +d        +e        +f+  "│\n"
			  "│  └───┘  │  └───┘  │  └───┘  │\n"
			  "├─────────┼─────────┼─────────┤\n"
			  "│6 ┌───┐  │7 ┌───┐  │8 ┌───┐  │\n"
			       +g        +h        +i+  "│\n"
			  "│  └───┘  │  └───┘  │  └───┘  │\n"
			  "└─────────┴─────────┴─────────┘\n"

			  )

	def convertSymbols(self, x):  #converti les nombres en pion sur le plateau
		if x == 0:
			res = "│         "

		if x == 1:
			res = "│  │   │  "

		if x == 2:
			res = "│  │ O │  "

		if x == 3:
			res = "│  │ X │  "

		return res 

	def is_finished(self): #fonction détectant si il y a une victoire

	    if (self.state[0]==self.state[1]) and (self.state[0]==self.state[2]) and ((self.state[0]==2) or (self.state[0]==3)):
	        return True
	    if (self.state[3]==self.state[4]) and (self.state[3]==self.state[5]) and ((self.state[3]==2) or (self.state[3]==3)):
	        return True
	    if (self.state[6]==self.state[7]) and (self.state[6]==self.state[8]) and ((self.state[6]==2) or (self.state[6]==3)):
	        return True
	    if (self.state[0]==self.state[3]) and (self.state[0]==self.state[6]) and ((self.state[0]==2) or (self.state[0]==3)):
	        return True
	    if (self.state[1]==self.state[4]) and (self.state[1]==self.state[7]) and ((self.state[1]==2) or (self.state[1]==3)):
	        return True
	    if (self.state[2]==self.state[5]) and (self.state[2]==self.state[8]) and ((self.state[2]==2) or (self.state[2]==3)):
	        return True
	    if (self.state[0]==self.state[4]) and (self.state[0]==self.state[8]) and ((self.state[0]==2) or (self.state[0]==3)): 
	        return True
	    if (self.state[2]==self.state[4]) and (self.state[2]==self.state[6]) and ((self.state[2]==2) or (self.state[2]==3)):
	        return True
	    else:
	    	return False

def clear_console():

    if name == 'nt': 
        _ = system('cls') 
 
    else: 
        _ = system('clear')

def display_game(game):
	game.display()

def play(game,p1,p2):  #fonction permettant de faire jouer 2 joueurs

	game.reset()

	players = [p1,p2]

	random.shuffle(players)

	p=0
	quit_game = False	

	while game.is_finished() is False and quit_game is False: #tant que la partie est pas terminée
		action = -1
		p+=1
		clear_console()
		game.display()

		if players[p%2].is_human is True: #si le joueur est humain, il joue

			while action < 0 or action > 3:
				if (players[p%2] == p1):
					print(" C'est au tour des cercles\n")
				else:
					print(" C'est au tour des croix\n")

				action = int(input("\n Choisissez une action \n\n\n 0 : Quitter la partie \n\n 1 : Placer un pion \n 2 : Déplacer un carré\n 3 : Déplacer un pion\n\n"))
				
				if action == 0:
					quit_game = True
					break
				if action == 1:
					if players[p%2].pion_remaining == 0:
						print("\n Vous n'avez plus de pions !\n")
						action = -1
						sleep(2)

				if action == 3:
					if players[p%2].pion_remaining == 3:
						print("\n Vous n'avez pas de pions à déplacer !\n")
						action = -1
						sleep(2)

				if action < 0 or action > 3:
					clear_console()
					game.display()


			if action > 0 and action < 4:
				new_state = players[p%2].action_player(action,game.state,game,players[(p%2)-1]) #à partir de l'action du joueur, crée le nouvel état du plateau

				game.state = new_state   #l'état du jeu change
			
			if (game.is_finished()==True):  #détection de victoire

				if (players[p%2] == p1):
					print("\n Les cercles gagnent !\n")
					break
				else:
					print("\n Les croix gagnent !\n")
					break						



		elif players[p%2].is_human is False: #si le joueur est une IA, elle joue

			print("l'IA joue")



if __name__ == '__main__':


	game = Game()

	human1 = Player(is_human = True, pion_choice = "circle")
	human2 = Player(is_human = True, pion_choice = "cross")

	ordi1 = Player(is_human = False, pion_choice = "circle")
	ordi2 = Player(is_human = False, pion_choice = "cross")


	play(game,human1,human2)

	


