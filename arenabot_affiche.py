# Simple script that simulates a bot moving inside an Arena, following a series of commands
# by Alberto Tonda, 2018 <alberto.tonda@gmail.com>

import sys
import inspyred
import random
import numpy as np


random_number_generator = random.Random()
random_number_generator.seed(40)


# instantiate the evolutionary algorithm object
evolutionary_algorithm = inspyred.ec.EvolutionaryComputation(random_number_generator)
# and now, we specify every part of the evolutionary algorithm
evolutionary_algorithm.selector = inspyred.ec.selectors.tournament_selection # by default, tournament selection has tau=2 (two individuals), but it can be modified (see below)
evolutionary_algorithm.variator = [inspyred.ec.variators.uniform_crossover] # the genetic operators are put in a list, and executed one after the other
evolutionary_algorithm.replacer = inspyred.ec.replacers.plus_replacement # "plus" -> "mu+lambda"
evolutionary_algorithm.terminator = inspyred.ec.terminators.evaluation_termination # the algorithm terminates when a given number of evaluations (see below) is reached

evolutionary_algorithm.observer = inspyred.ec.observers.plot_observer 

'''This function accepts in input a list of strings, and tries to parse them to update the position of a robot. Then returns distance from objective.'''
def fitnessRobot(listOfCommands, visualize=False) :

	# the Arena is a 100 x 100 pixel space
	arenaLength = 100
	arenaWidth = 100
	
	# let's also put a couple of walls in the arena; walls are described by a set of 4 (x,y) corners (bottom-left, top-left, top-right, bottom-right)
	walls = []

	wall1 = dict()
	wall1["x"] = 30
	wall1["y"] = 0
	wall1["width"] = 10
	wall1["height"] = 80

	wall2 = dict()
	wall2["x"] = 70
	wall2["y"] = 20
	wall2["width"] = 10
	wall2["height"] = 80

	walls.append(wall1)
	walls.append(wall2)
	
	# initial position and orientation of the robot
	startX = robotX = 10
	startY = robotY = 10
	startDegrees = 90 # 90°
	
	# position of the objective
	objectiveX = 90
	objectiveY = 90
	
	x=90
	y=90
	
	# this is a list of points that the robot will visit; used later to visualize its path
	positions = []
	positions.append( [robotX, robotY] )
		
	# TODO move robot, check that the robot stays inside the arena and stop movement if a wall is hit
	#listOfCommands est de la forme ["move 20","rotate 90",...,]
	for command in listOfCommands:
		tab=command.split()
		mode=tab[0]
		deplacement=tab[1]
		deplacement=int(deplacement)
		#print(mode,deplacement)
		
		if mode=="rotate":
			startDegrees=(startDegrees+deplacement)%360
			#print(startDegrees,"degrés")

		elif mode=="move":
			etat_mur=0
			etat_premier_mur=1
		#le robot va à droite
			if startDegrees==0:
				
				#on parcourt tous les murs
				for wall in walls :
				
					#si le robot a croisé un mur
					if robotX < wall["x"] and robotX+deplacement>=wall["x"]and (wall["y"]<=robotY<=wall["y"]+wall["height"]):
						#on indique que le robot a croisé un mur
						etat_mur=1
						
						#si c'est le premier mur touché
						if etat_premier_mur==1 :
							proche_mur=wall
							etat_premier_mur=0

						#on actualise le mur le plus proche
						if wall["x"]<proche_mur["x"]:
							proche_mur=wall
				
				if etat_mur==1:
					robotX=proche_mur["x"]-1
				elif etat_mur==0:
					robotX=min(robotX+deplacement,99)
		
			#le robot va en haut
			elif startDegrees==90:

				for wall in walls :
					#print(wall["y"])
					#si le robot a croisé un mur
					if ((robotY < wall["y"]) and (robotY+deplacement>=wall["y"]) and (wall["x"]<=robotX<=wall["x"]+wall["width"])):
						#on indique que le mur a croisé un mur
						etat_mur=1
						
						#si c'est le premier mur touché
						if etat_premier_mur==1 :
							proche_mur=wall
							etat_premier_mur=0
							
							
						#on actualise le mur le plus proche
						if wall["y"]<proche_mur["y"]:
							proche_mur=wall
			
				if etat_mur==1:
					robotY=proche_mur["y"]-1
				elif etat_mur==0:
					robotY=min(robotY+deplacement,99)
				
				
			#le robot va à gauche
			elif startDegrees==180:
				for wall in walls :
					
					#si le robot a croisé un mur
					if (robotX > wall["x"]+wall["width"]) and (robotX-deplacement<=wall["x"]+wall["width"]) and (wall["y"]<=robotY<=wall["y"]+wall["height"]):
						#on indique que le mur a croisé un mur
						etat_mur=1
						
						#si c'est le premier mur touché
						if etat_premier_mur==1 :
							proche_mur=wall
							etat_premier_mur=0
						
						#on actualise le mur le plus proche
						if wall["x"]>proche_mur["x"]:
							proche_mur=wall
				
				if etat_mur==1:
					robotX=proche_mur["x"] +1+proche_mur["width"]
				elif etat_mur==0:
					robotX=max(robotX-deplacement,1)
			
				
				
			#le robot va en bas 
			elif startDegrees==270:
				for wall in walls :
				
					#si le robot a croisé un mur
					if robotY > (wall["y"]+wall["height"]) and robotY-deplacement<=(wall["y"]+wall["height"]) and (wall["x"]<=robotX<=wall["x"]+wall["width"]):
						#on indique que le mur a croisé un mur
						etat_mur=1
						
						#si c'est le premier mur touché
						if etat_premier_mur==1 :
							proche_mur=wall
							etat_premier_mur=0
							
						#on actualise le mur le plus proche
						if wall["y"]>proche_mur["y"]:
							proche_mur=wall
			
				if etat_mur==1:
					robotY=proche_mur["y"] +proche_mur["height"] + 1
				elif etat_mur==0:
					robotY=max(robotY-deplacement,1)
					
		positions.append( [robotX, robotY] )


	# TODO measure distance from objective

	distanceFromObjective = abs(robotX-objectiveX) + abs(robotY-objectiveY)
	
	
	
	# this is optional, argument "visualize" has to be explicitly set to "True" when function is called
	if visualize :
		
		import matplotlib.pyplot as plt
		import matplotlib.patches as patches
		figure = plt.figure()
		ax = figure.add_subplot(111)
		
		# plot initial position and objective
		ax.plot(startX, startY, 'r^', label="Initial position of the robot")
		ax.plot(objectiveX, objectiveY, 'gx', label="Position of the objective")
		
		# plot the walls
		for wall in walls :
			ax.add_patch(patches.Rectangle( (wall["x"], wall["y"]), wall["width"], wall["height"] ))
		
		# plot a series of lines describing the movement of the robot in the arena
		for i in range(1, len(positions)) :
			ax.plot( [ positions[i-1][0], positions[i][0] ], [ positions[i-1][1], positions[i][1] ], 'r-' )
		
		ax.set_title("Movements of the robot inside the arena")
		#ax.legend(loc='best')
		plt.show()

	return distanceFromObjective


def evaluator_arenabot(candidates,args) :
	list_of_fitness_values = []

	# iterate over all the candidates, run the Weierstrass function, append result to list
	for candidate in candidates :
		fitness_value = fitnessRobot(candidate)
		list_of_fitness_values.append(fitness_value)

	return list_of_fitness_values
	
#This function accepts in input a list of strings, and tries to parse them to update the position of a robot. Then returns distance from objective.
def commande_au_hasard(proba):
	# proba d'avoir un move
	p=random_number_generator.uniform(0,1)
	if p<=proba:
		x="move"
		value_move=random.randint(1,90)
		return(x+' '+str(value_move))
	else:
		x="rotate"
		value_rotate=random.choice([90,180,270])
		#print(x,value_rotate)
		return(x+' '+str(value_rotate))

def generator_arenabot(random,args):
	taille_liste=random.randint(1,args["max_taille_liste"])
	individual = [ commande_au_hasard(args["prob_move"]) for x in range(0, taille_liste) ] #ici l'individu est une liste de commande  
	return individual
	




################# MAIN
def main() :
	#Copier coller ici la liste de commande trouvée dans arenabot_cross
	listOfCommands=['move 18', 'move 68', 'move 60', 'move 4', 'move 28', 'move 21', 'rotate 90', 'move 80', 'rotate 90', 'rotate 90', 'move 87', 'rotate 270', 'move 63', 'move 28', 'rotate 270', 'rotate 270', 'move 23', 'rotate 180', 'move 89', 'move 14', 'move 15', 'rotate 90', 'move 56', 'move 15', 'rotate 270', 'move 83', 'move 5', 'rotate 180', 'rotate 270', 'move 12', 'rotate 90', 'move 77', 'move 18', 'move 76', 'move 57', 'rotate 180', 'move 85', 'move 65', 'move 79', 'move 76', 'move 70', 'move 68', 'rotate 180', 'move 20', 'move 24', 'move 1', 'move 32', 'move 77', 'move 54', 'move 44', 'move 26', 'rotate 270', 'move 62', 'move 16', 'rotate 180', 'rotate 270', 'rotate 270', 'move 84', 'rotate 270']

	fitnessRobot(listOfCommands,visualize=True)
	return 0

if __name__ == "__main__" :
	sys.exit( main() )

