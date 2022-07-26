import time
from turtle import position
import renderConstants
import random as rd
from Animator import Animations
from Animator import Animation
class ZombieAI :
    currentState = "Roam"
    active = False
    states = ["Roam", "Seek", "Attack"]
    seekPosition = [1, 1]
    classID = 0
    position = [2,2]
    board = None
    vision = 4
    
    
    def __init__(self):
        self.active = True
        self.ID = ZombieAI.classID #creates the ID for the current Ai, for every AI increase by 1
        ZombieAI.classID += 1

    def performAction(self, board): 
        self.positionUpdate(board) 
        if(self.currentState != self.states[0]):
            self.setState(0, board)
        self.seekPosition = board.findPlayer() #coords the player one
        if abs(self.seekPosition[0] - self.position[0]) + abs(self.seekPosition[1] - self.position[1]) <= self.vision: #a vision scenario: seek
            self.setState(1, board)
        if board.isAdjacentTo(self.position,False): #a vision scenario: attack
            self.setState(2, board) 
        stateactions = {
            "Roam" : self.stateRoam(board),
            "Attack" : self.stateAttack(board),
            "Seek" : self.stateSeek(board)
        }
        action = stateactions[self.currentState] #return the value
        return action
    def setState(self, state, board):
        self.currentState = self.states[state]
        if(self.currentState == "Roam"):
            board.States[self.position[1]][self.position[0]].person.animation = Animation(Animations.zombie.value)
        elif(self.currentState == "Attack"):
            board.States[self.position[1]][self.position[0]].person.animation = Animation(Animations.bite.value)
        elif(self.currentState == "Seek"):
            board.States[self.position[1]][self.position[0]].person.animation = Animation(Animations.seek.value)
    def positionUpdate(self, gameBoard):
        self.position = gameBoard.findPerson(self.ID)

    def stateSeek(self, board):           
        if self.seekPosition == self.position: #back to Roam
            self.setState(0)
        possiblemoves = self.getLegalMoves(board) #gets all possible move 
        prevDistance = abs(self.seekPosition[0] - self.position[0]) + abs(self.seekPosition[1] - self.position[1]) 
        if(len(possiblemoves) == 0): #no posible moves exist
            chosenMove = self.position
        else: 
            chosenMove = possiblemoves[0]
            #find the position that is the closest to the human
        for Move in possiblemoves:
            distance = abs(self.seekPosition[0] - (Move[0])) + abs(self.seekPosition[1] - (Move[1]))
            if prevDistance > distance:
                prevDistance = distance 
                chosenMove = Move
        return ("move", chosenMove, "seek") #Added third data value for Animation

    def stateAttack(self, board):
        #Bite at the seeked position
        return ("bite", self.seekPosition)

    def stateRoam(self, gameBoard):
        possibleMoves = self.getLegalMoves(gameBoard)
        if len(possibleMoves) > 0: #if theres no possibleMovement rd crashes
            move = rd.choice(possibleMoves) 
        else: 
            move = self.position #stay there
        return ("move", move, "roam")

    def getLegalMoves(self, gameBoard): #legal moves for this zombie
        possible_move_coords = []
        
        vals = [
            (self.position[0], self.position[1] + 1),
            (self.position[0], self.position[1] - 1),
            (self.position[0] + 1, self.position[1]),
            (self.position[0] - 1, self.position[1]),
        ]
        for coordinate in vals:
            if gameBoard.isValidCoordinate(coordinate) and gameBoard.States[coordinate[1]][coordinate[0]].person == None:
                if gameBoard.States[coordinate[1]][coordinate[0]].passable() == True:
                     possible_move_coords.append(coordinate)
        return possible_move_coords