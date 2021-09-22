import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from fruit import Fruit
from sprites import MazeSprites
import numpy as np
import pprint
from timeit import default_timer as timer
from pellets import Pellet, PelletGroup
from queue import PriorityQueue


class SearchControl(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock() 
        self.fruit = None
        


    

    def search(self):
        startX, startY = 1, 31
        endX, endY = 26, 4
        startNode = self.nodes.nodesLUT[(startX * 16, startY * 16)]
        endNode = self.nodes.nodesLUT[(endX * 16, endY * 16)]
        startUFC = timer()
        self.ufc(startNode, endNode)
        endUFC = timer()
        print(str(endUFC - startUFC)+" -- ufc")
        startDFS = timer()
        self.dfs(startNode, endNode)
        endDFS = timer()
        print(str(endDFS - startDFS)+" -- dfs")
        startBFS = timer()
        self.bfs(startNode, endNode)
        endBFS = timer()
        print(str(endBFS - startBFS)+" -- bfs")
       
        

    def bfs(self, startNode, endNode):
        visited = []
        queue = [(startNode,[startNode])]
        visited.append(startNode)
        while queue:
            current, path = queue.pop(0) 

            for neighbour in self.nodes.nodesLUT[current.position.asTuple()].neighbors:
                if self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour] not in visited and self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]:
                    visited.append(self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour])
                    queue.append([self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour], (path + [self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]])])
                    if self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour] == endNode:
                        path.append(endNode)
                        for x in path:
                            print(x.position.__str16__())
                        return path

    def dfs(self, startNode, endNode):
        visited = []
        stack = [(startNode,[startNode])]
        
        visited.append(startNode)


        while stack:
            current, path = stack.pop() 
           
            
            for neighbour in self.nodes.nodesLUT[current.position.asTuple()].neighbors:
                #print(self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]) 
                if self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour] not in visited and self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]:
                    visited.append(self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour])
                    stack.append([self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour], (path + [self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]])])
                    if self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour] == endNode:
                        path.append(endNode)
                        for x in path:
                            print(x.position.__str16__())
                        return path
    


    def checkForPellet(self, node):
        for x in self.pellets.pelletList:
            if x.position == node.position:
                return x.name

    def ufc(self, startNode, endNode):
        visited = []
        ident = 0
        pqueue = PriorityQueue()
        pqueue.put((0, (ident, startNode, [startNode])))  #cost, node, path
        while pqueue:

            cost, bunch  = pqueue.get() 
            
            current = bunch[1] 
            path = bunch[2]
            if current not in visited: # check to avoid duplicate expansions
                visited.append(current)
            #print(queue)
            if current == endNode:
                for x in path:
                    print(x.position.__str16__())
                return path
            else:
                for neighbour in self.nodes.nodesLUT[current.position.asTuple()].neighbors:
                    
                    if self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour] not in visited and self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]:
                        #check for cost
                        ident+=1
                        newCost = 0
                        for x in self.pellets.pelletList:
                            if x.position == self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour].position:
                                objectName = x.name
                        if objectName == PELLET:
                            newCost = 50
                        elif objectName == POWERPELLET:
                            newCost = -100
                        else:
                            newCost = 100
                        pqueue.put((cost + newCost, (ident, self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour], path + [self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]])))
                    
    

    def update(self):
        dt = self.clock.tick(30) / 1000.0 
        self.pacman.update(dt)
        if self.fruit is not None:
            #self.fruit.update(dt)
            self.checkFruitEvents()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                #add search
                if event.key == K_s:
                    self.pacman.visible = True
                    self.ghosts.hide()


    def checkFruitEvents(self):  
        if self.fruit is None:
            self.fruit = Fruit(self.nodes.getNodeFromTiles(26, 4))
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None
    
    def setBackground(self):
            self.background = pygame.surface.Surface(SCREENSIZE).convert()
            self.background.fill(BLACK)
    
    def startGame(self):
        self.setBackground()
        self.mazesprites = MazeSprites("maze.txt", "rotation.txt")
        self.background = self.mazesprites.constructBackground(self.background, 2)
        self.nodes = NodeGroup("maze.txt")
        self.fruit = Fruit(self.nodes.getNodeFromTiles(26, 4))
        self.nodes.setPortalPair((0,17), (27,17))
        self.pacman = Pacman(self.nodes.getNodeFromTiles(1, 32))#we start here
        self.pellets = PelletGroup("maze.txt")

    def render(self):
        self.screen.blit(self.background, (0, 0))
        #for skeleton purpose
        self.nodes.render(self.screen)
        self.pellets.render(self.screen) 
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        pygame.display.update()

pygame.display.set_caption('Lady Pacman')    
if __name__ == "__main__":
    game = SearchControl()
    game.startGame()
    game.search()
    while True:
        game.update()

    

    
