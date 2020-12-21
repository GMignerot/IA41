from os import system, name
from time import sleep 
from Game import display_game

class Player:

	def __init__(self,is_human,pion_choice):
		self.is_human = is_human
		self.pion_choice = pion_choice
		self.pion_remaining = 3

	def action_player(self, action, etat,game):  #les 3 coups possible d'un joueur

		if action == 1:  # 1 : action de placer un pion

			coord_place_pion = -1
			valid_placement = False

			while coord_place_pion < 0 or coord_place_pion > 8 or valid_placement is not True:  #tant que la coordonnée pour placer un pion est pas bonne, on demande la coordonnée

				coord_place_pion = int(input("\n "+str(self.pion_remaining)+" pions restants\n\n Ou voulez vous placer votre pion ? (0 à 8)\n\n"))
				if coord_place_pion<0 or coord_place_pion > 8:
					print("\n Merci de mettre un nombre entre 0 et 8\n")

				elif etat[coord_place_pion] != 1 :
					print("\n Cette case est déjà occupée !\n")
					sleep(2)
					clear_console()
					display_game(game)

				elif etat[coord_place_pion] == 1: #si la case est libre alors le placement est valide
					valid_placement = True

			new_etat = self.place_pion(coord_place_pion,etat) #on place le pion, la fonction retourne le nouvel état

			self.pion_remaining -= 1

			return new_etat

		if action == 2: # 2 : action de déplacer un carré

			new_etat = self.move_square(etat,game)	

			return new_etat

		if action == 3:  # 3 : action de déplacer un pion

			new_etat = self.move_pion(etat,game)
			return new_etat

	def place_pion(self,coord_place_pion,etat): #place un pion sur le plateau

		if self.pion_choice == "circle":
			etat[coord_place_pion] = 2
			new_etat = etat

		elif self.pion_choice == "cross":
			etat[coord_place_pion] = 3
			new_etat = etat


		return new_etat

	def move_square(self,etat,game):  #permet de déplacer un ou deux carrés sur le plateau

		empty_list = [[1,2,3,6],[0,2,4,7],[0,1,5,8],[0,4,5,6],[1,3,5,7],[2,3,4,8],[0,3,7,8],[1,4,6,8],[2,5,6,7]] #si la case vide est en 0, le joueur peut déplacer le carré 1, 2, 4 et 6 mais pas les autres

		for i in range(9):
			if etat[i]==0:
				empty_case = i

		possible_move = empty_list[empty_case]

		valid_coord = False
		while valid_coord is False:  #on s'assure que le carré qu'on veut déplacer est déplacable

			coord_square = int(input("\n Quel carré voulez vous déplacer ? "+str(possible_move)+"\n"))
			for i in range(4):
				if possible_move[i] == coord_square:
					valid_coord = True

			if valid_coord is False:
				print("\n Vous ne pouvez pas déplacer ce carré, réessayez\n")
				sleep(2)
				clear_console()
				display_game(game)
		
		new_etat = etat
                           							#l'énorme pavé là permet de gérer toutes les poussées doubles
		if empty_case == 0 and coord_square==2:
				new_etat[empty_case]=etat[1]
				new_etat[1]=etat[2]
				new_etat[2] = 0

		elif empty_case == 0 and coord_square==6:
				new_etat[empty_case]=etat[3]
				new_etat[3]=etat[6]
				new_etat[6] = 0		

		elif empty_case == 1 and coord_square==7:
				new_etat[empty_case]=etat[4]
				new_etat[4]=etat[7]
				new_etat[7] = 0		

		elif empty_case == 2 and coord_square==0:
				new_etat[empty_case]=etat[1]
				new_etat[1]=etat[0]
				new_etat[0] = 0	

		elif empty_case == 2 and coord_square==8:
				new_etat[empty_case]=etat[5]
				new_etat[5]=etat[8]
				new_etat[8] = 0	

		elif empty_case == 3 and coord_square==5:
				new_etat[empty_case]=etat[4]
				new_etat[4]=etat[5]
				new_etat[5] = 0	

		elif empty_case == 5 and coord_square==3:
				new_etat[empty_case]=etat[4]
				new_etat[4]=etat[3]
				new_etat[3] = 0

		elif empty_case == 6 and coord_square==0:
				new_etat[empty_case]=etat[3]
				new_etat[3]=etat[0]
				new_etat[0] = 0	

		elif empty_case == 6 and coord_square==8:
				new_etat[empty_case]=etat[7]
				new_etat[7]=etat[8]
				new_etat[8] = 0	

		elif empty_case == 7 and coord_square==1:
				new_etat[empty_case]=etat[4]
				new_etat[4]=etat[1]
				new_etat[1] = 0	

		elif empty_case == 8 and coord_square==2:
				new_etat[empty_case]=etat[5]
				new_etat[5]=etat[2]
				new_etat[2] = 0	

		elif empty_case == 8 and coord_square==6:
				new_etat[empty_case]=etat[7]
				new_etat[7]=etat[6]
				new_etat[6] = 0	
		else:
			new_etat[empty_case]=etat[coord_square]  #poussée simple
			new_etat[coord_square]=0

		return new_etat

	def move_pion(self,etat,game): #permet de déplacer un pion du plateau

		new_etat = etat

		if self.pion_choice == "cross":
			cross_playing = True
		else:
			cross_playing = False

								 #si la case vaut 2 et que c'est les croix qui joue, pas bon
								 #si la case vaut 3 et que c'est les ronds qui joue, pas bon

		while(True):

			coord_pion = int(input("\n Quel pion voulez-vous déplacer ? \n\n"))
			if etat[coord_pion] == 2 and cross_playing is True:
				print("\n Prenez un pion croix ! \n")
				sleep(2)
				clear_console()
				display_game(game)				

			elif etat[coord_pion] == 3 and cross_playing is not True:
				print("\n Prenez un pion cercle !\n") 
				sleep(2)
				clear_console()
				display_game(game)

			elif etat[coord_pion] == 0 or etat[coord_pion] == 1:
				print("\n Prenez un pion valide !\n") 
				sleep(2)
				clear_console()
				display_game(game)				
			else:
				break
				
		while(True):
			coord_final = int(input("\n Ou voulez vous placer ce pion ?\n"))

			if etat[coord_final]!=1:
				print("\n Veuillez choisir un emplacement valide !\n")
				sleep(2)
				clear_console()
				display_game(game)				
			else:
				if cross_playing is True:
					new_etat[coord_final] = 3
				else:
					new_etat[coord_final] = 2
				new_etat[coord_pion]=1
				break

		return new_etat
def clear_console():

    if name == 'nt': 
        _ = system('cls') 
 
    else: 
        _ = system('clear')
