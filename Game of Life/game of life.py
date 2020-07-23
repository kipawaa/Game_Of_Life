#game of life
''' TO DO: '''
#FIX function to handle each type of cell's advancement through generations (parameters will be live and will output the cell's new value)

from graphics import *
from Graphics_Functions import *
from random import random, randint
from time import time

#prepares a Zelle Graphics window to be used
def prepGraphicsWindow(title, width, height):
   win = GraphWin(title, width, height, autoflush = False)
   return win

#generates a random starting generation for Conway's Game of Life as a 2D array
def firstGen(width, height):
    print('Creating the seed...')
    arr = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(randint(0, 1))
        arr.append(row)
    return arr

#takes an array representing a generation of Conway's Game of Life and progresses it by one generation
        #FUTURE: potentially jump many generations?
def getGen(arr):
    #print('Proceeding to Next Generation...')
    newArr = [[j for j in i] for i in arr]
    
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            #change according to rules
            ''' rules:
                < 2 = dead
                2-3 = continue
                3   = life
                > 3 = dead
                any cell next to, including diagonal, counts to population
            '''
            
            #holds the number of surrounding live cells
            live = 0

            #holds the cells to be checked
            checks = []
            
            #adds the values of all surrounding cells to a list
            if i == 0:
                if j == 0:
                    checks += [arr[i][j+1], arr[i+1][j], arr[i+1][j+1]]
                elif j == len(arr[i])-1:
                    checks += [arr[i][j-1], arr[i+1][j-1], arr[i+1][j]]
                else:
                    checks += [arr[i][j-1], arr[i][j+1], arr[i+1][j-1], arr[i+1][j], arr[i+1][j-1]]
            elif i == len(arr)-1:
                if j == 0:
                    checks += [arr[i-1][j], arr[i-1][j+1], arr[i][j+1]]
                elif j == len(arr[i])-1:
                    checks += [arr[i-1][j-1], arr[i-1][j], arr[i][j-1]]
                else:
                    checks += [arr[i-1][j-1], arr[i-1][j], arr[i-1][j+1], arr[i][j-1], arr[i][j+1]]
            else:
                if j == 0:
                    checks += [arr[i-1][j], arr[i-1][j+1], arr[i][j+1], arr[i+1][j], arr[i+1][j+1]]
                elif j == len(arr[i])-1:
                    checks += [arr[i-1][j-1], arr[i-1][j], arr[i][j-1], arr[i+1][j-1], arr[i+1][j]]
                else:
                    checks += [arr[i-1][j-1], arr[i-1][j], arr[i-1][j+1], arr[i][j-1], arr[i][j+1], arr[i+1][j-1], arr[i+1][j], arr[i+1][j+1]]

            #controls whether toxic and immortal cells are used
            useImmortal = True
            useToxic = True
            
            #counts the number of live cells
            for k in checks:
               #if the value of a cell is greater than 0 adds 1 to live
               if k > 0:
                  live += 1
               #if the value of a cell is negative 1 subtracts 1 from live
               elif k == -1:
                  live -= 1

            #checks the live value and cell status and updates the cell accordingly
            #print(arr[i][j])
            arr[i][j] = checkCell(live, arr[i][j], False, False)
    return newArr

def checkCell(live, cell, useToxic, useImmortal):
   #changes cells based on the number of surrounding live cells
   ''' MODIFIED RULES: '''
   ''' if live == 8 (completely surrounded) cell becomes immortal '''
   ''' if live == 0 (nothing around) cell becomes toxic '''
   
   #checks if cell value is 2 (immortal) and maintains it
   if cell == 2:
      return 2
   #checks if cell value is -1 (toxic) and maintains it
   elif cell == -1:
      return -1
   #handles all cells that are not immortal or toxic
   else:
      #creates immortal cell if conditions are met (conditions are in MODIFIED RULES in the large comment section)
      if live == 8 and useImmortal == True:
         return 2
      #creates toxic cell if conditions are met
      elif live == 0 and useToxic == True:
         return -1
      #kills cells if their area is under or over populated
      elif live < 2 or live > 3:
         return 0
      #creates a cell if conditions are met
      elif live == 3:
         return 1
      else:
         return cell

#allows for the visual representation of Conway's Game of Life in a Zelle Graphics window
def visualize(arr, win):
    clearWin(win)
    for i in range(len(arr)):
        for j in range(len(arr[i])):

            if arr[i][j] == 0:
                colour = 'black'
            elif arr[i][j] == 2:
               colour = 'green'
            elif arr[i][j] == -1:
               colour = 'red'
            else:
                colour = 'white'

            rect = drawRect(j/len(arr[i])*1280, i/len(arr)*710, 1280/len(arr[i]), 710/len(arr), colour)
            rect.draw(win)
    update()

#runs a simulation of Conway's Game of Life with Zelle Graphics
def graphicsRun():
   overallTime = time()
   #creates a window
   win = prepGraphicsWindow('Game of Life', 1280, 710)

   #creates the first generation
   lastGen = firstGen(128, 71)

   #records the number of generations passed
   generationNumber = 0

   #boolean for whether or not to draw each generation
   doVisualize = True

   #runs the simulation continuously
   while True:
      #records time at the start of each generation
      start = time()

      #creates visual representation of the simulation for each generation if doVisualize is True
      if doVisualize:
         visualize(lastGen, win)

      #creates a new generation based on the last
      lastGen = getGen(lastGen)

      #increments and prints the number of generations passed
      generationNumber += 1
      print(generationNumber, time() - start)

      key = win.checkKey()

      if key == 'g':
         lastGen = firstGen(128, 71)
         generationNumber = 0
      elif key == 'p':
         win.getKey()
      elif key == 'd':
         if doVisualize == False:
            doVisualize = True
         else:
            doVisualize = False
      elif key == 't':
         print('Program Time:', time()-overallTime)
      elif key == 'q':
         win.close()

graphicsRun()
