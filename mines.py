# -*- coding: utf-8 -*-
"""minesweeper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1COgxYvXme--t2WRaoYKmBIH98f0PmFA2
"""

import random
import re
import time


class Mines:
    def __init__(self, gridsize, numberofmines):
        self.flags = []
        self.__currgrid = [[' ' for i in range(gridsize)] for i in range(gridsize)]
        self.__fail = False
        self.__currcell = (0,0)
        emptygrid = [['0' for i in range(gridsize)] for i in range(gridsize)]
        self.__mines = self.__getmines(emptygrid, self.__currcell, numberofmines)        
        for i, j in self.__mines:
            emptygrid[i][j] = 'X'
        self.__grid = self.__getnumbers(emptygrid)                

        
    def __getrandomcell(self, grid):
        gridsize = len(grid)

        a = random.randint(0, gridsize - 1)
        b = random.randint(0, gridsize - 1)

        return (a, b)

    def __getneighbors(self, grid, rowno, colno):
        gridsize = len(grid)
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif -1 < (rowno + i) < gridsize and -1 < (colno + j) < gridsize:
                    neighbors.append((rowno + i, colno + j))
                    
        return neighbors
    

    def __getmines(self, grid, start, numberofmines):
        mines = []
        neighbors = self.__getneighbors(grid, *start)

        for i in range(numberofmines):
            cell = self.__getrandomcell(grid)
            while cell == start or cell in mines or cell in neighbors:
                cell = self.__getrandomcell(grid)
            mines.append(cell)
            
        return mines
    

    def __getnumbers(self, grid):
        for rowno, row in enumerate(grid):
            for colno, cell in enumerate(row):
                if cell != 'X':
                    values = [grid[r][c] for r, c in self.__getneighbors(grid, rowno, colno)]
                    grid[rowno][colno] = str(values.count('X'))
                    
        return grid
    
    
    def __showcells(self, rowno, colno):        
        if self.__currgrid[rowno][colno] != ' ':
            return

        self.__currgrid[rowno][colno] = self.__grid[rowno][colno]

        if self.__grid[rowno][colno] == '0':
            for r, c in self.__getneighbors(self.__grid, rowno, colno):
                if self.__currgrid[r][c] != 'F':
                    self.__showcells(r, c)
                    

    def __showgrid(self, grid):
        gridsize = len(grid)
        horizontal = '   ' + (4 * gridsize * '-') + '-'
        toplabel = '     '

        for i in range(gridsize):
            if i < 10:
                toplabel = toplabel + str(i) + '   '
            else:
                toplabel = toplabel + str(i) + '  '

        print(toplabel + '\n' + horizontal)

        for idx, i in enumerate(grid):
            row = '{0:2} |'.format(idx)
            for j in i:
                row = row + ' ' + j + ' |'

            print(row + '\n' + horizontal)

        print('')
    

    def checkcell(self, cell):
        if not self.__fail:            
            self.__currcell = cell
            if self.__grid[cell[0]][cell[1]] == 'X':
                self.__fail = True
                
        return self.__currgrid


    def showcurrent(self):        
        self.__showcells(*self.__currcell)
        self.__showgrid(self.__currgrid)

    
    def isfail(self):
        return self.__fail


    def checkmines(self):
        if set(self.__mines) == set(self.flags):
            return True
        else:
            return False

        
if __name__ == '__main__':
    gridsize = int(input("Enter Grid Size: "))
    n_mines = int(input("Enter Number of Mines: "))
    sweeper = Mines(gridsize, n_mines)
    sweeper.showcurrent()

import copy

#gets the neighbors of the current cell
def getNeighbors(grid, row, col):
  neighbors = []
  for i in range(-1, 2):
      for j in range(-1, 2):
          if i == 0 and j == 0:
              continue
          elif -1 < (row + i) < gridsize and -1 < (col + j) < gridsize:
              neighbors.append((row + i, col + j))
  return neighbors

#returns the flags in the list of neighbors
def getFlags(grid, neighbors, minesweeper):
  totalFlags = 0
  for n in neighbors:
    if n in minesweeper.flags:
      totalFlags = totalFlags + 1
  return totalFlags

#returns the number of empty spots in the list of neighbors
def getEmpty(grid, neighbors):
  totalEmpty = 0
  for n in neighbors:
    if grid[n[0]][n[1]] == " ":
      totalEmpty = totalEmpty + 1
  return totalEmpty

#returns the empty neighbors coordinates in the list of neighbors
def getEmptyNeighbors(grid, neighbors):
  emptyNeighbors = []
  for n in neighbors:
    if grid[n[0]][n[1]] == " ":
      emptyNeighbors.append((n[0],n[1]))
  return emptyNeighbors

#for rules 1 and 2
def simpleLogic(minesweeper, grid, row, col):
  #print('row: ',row)
  #print('col: ',col)
  currentNumber = int(grid[row][col])
  #finds neighbors
  neighbors = getNeighbors(grid, row, col)
  #get the surrounding flags if any
  numFlags = getFlags(grid, neighbors, minesweeper)
  #get the surrounding empty squares
  numEmpty = getEmpty(grid, neighbors) - numFlags
  #rule 1
  #print(currentNumber, numFlags, numEmpty)
  if currentNumber - numFlags == numEmpty:
    for n in neighbors:
      if grid[n[0]][n[1]] == " ":
        if n not in minesweeper.flags:
          minesweeper.flags.append(n)
                    

  #rule 2
  if currentNumber == numFlags:
    for n in neighbors:
      if n in minesweeper.flags or grid[n[0]][n[1]]!= " ":
        continue
      else:
        a=n[0]
        b=n[1] 
        minesweeper.checkcell((a,b))
        for m in mines:
          if (a,b) is m:
            mines.remove((a,b))
        minesweeper.showcurrent()
  elif currentNumber - numFlags == 1:
    emptyN = getEmptyNeighbors(grid, neighbors)
    for n in emptyN:
      if n in minesweeper.flags:
        emptyN.remove(n)
    for mine in mines:
      mineLen = len(mine)
      currentLen = 0
      for square in mine:
        if square in emptyN:
          currentLen = currentLen + 1
      if currentLen == mineLen:
        for square in emptyN:
          if square not in mine:
            if square not in minesweeper.flags:
              minesweeper.checkcell(square)
              minesweeper.showcurrent()
              #for m in mines:
                #if square in m:
                  #mines.remove(m)
  #rule 3
  thirdRule(grid,row,col, minesweeper)  



#third rule
mines = []
def thirdRule(grid, row, col, minesweeper):
  currentNumber = int(grid[row][col])
  neighbors = getNeighbors(grid, row, col)
  #get the surrounding flags if any
  numFlags = getFlags(grid, neighbors, minesweeper)
  #get the surrounding empty squares
  numEmpty = getEmpty(grid, neighbors)
  if 1 == currentNumber - numFlags:
    #neighbors equal one bomb
    if getEmpty(grid, neighbors) > 0: # if it has multiple tiles around it
      mineCertain = []
      mineCertain.append((row,col))

      emptyNeighbors = getEmptyNeighbors(grid, neighbors)
      #indexOfNeighborWith1 = neighborNumbers.index(1)

      if emptyNeighbors not in mines:
        mines.append(getEmptyNeighbors(grid, neighbors))

#Game play loop
def main():
  start = time.time()
  it = 0
  minesweeper = copy.deepcopy(sweeper)
  restarts = -1
  pastBoard = minesweeper.checkcell((0, 0))
  while not minesweeper.checkmines():
    minesweeper = copy.deepcopy(sweeper)
    mines = []
    restarts = restarts + 1
    currentGrid = minesweeper.checkcell((0, 0))
    minesweeper.showcurrent()
    while not minesweeper.isfail() and not minesweeper.checkmines():
      for i in range(gridsize):
        for j in range(gridsize):
          #print("row", i, "col", j, minesweeper.flags)
          if currentGrid[i][j] != "0" and currentGrid[i][j] != " ":
            simpleLogic(minesweeper, currentGrid, i, j)
            minesweeper.showcurrent()

      if pastBoard == minesweeper.checkcell((0, 0)):
        it = it + 1
      else:
        it = 0
      pastBoard = minesweeper.checkcell((0, 0))
      while it == 5 and not minesweeper.checkmines():
          a = random.randint(0, gridsize - 1)
          b = random.randint(0, gridsize - 1)
          if (a,b) not in minesweeper.flags and currentGrid[a][b] == " ":
            minesweeper.checkcell((a,b))
            minesweeper.showcurrent()
            it = 0
        
  end = time.time()
  minesweeper.showcurrent()
  print("Win!")
  print("Total time taken:", end-start, "seconds")


main()

