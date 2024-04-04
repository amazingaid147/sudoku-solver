
class gridStack:
  def __init__(self):
      self.stack = []

  def GetSize(self):
      return len(self.stack)

  def push(self, grid):
      self.stack.append(grid)

  def pop(self):
      if self.GetSize() > 0:
          return self.stack.pop()
      else:
          return None

  def search(self, grid):
      return grid in self.stack


class treeSearch:
  def __init__(self, startSudoku, checkNextGridStack, VisitedGridStack, sudoku):
      self.startSudoku = startSudoku
      self.sudoku = sudoku
      self.checkNextGridStack = checkNextGridStack
      self.VisitedGridStack = VisitedGridStack

  def doDFS(self):
      for row in range(9):
          for column in range(9):
              self.startSudoku.SetSquare(row, column, self.sudoku[row][column])

      if self.startSudoku.isFinished():
          return self.startSudoku
      else:
          self.checkNextGridStack.push(self.startSudoku)
          while self.checkNextGridStack.GetSize() > 0:
              currentNode = self.checkNextGridStack.pop()
              if currentNode.isComplete():
                  return currentNode
              if not self.VisitedGridStack.search(currentNode):
                  self.VisitedGridStack.push(currentNode)
                  HasChildren = currentNode.HowManyChildren()
                  if HasChildren > 1:
                      for i in range(HasChildren):
                          potentialNodeGrid = currentNode.findChild(i, HasChildren)
                          self.checkNextGridStack.push(potentialNodeGrid)
      return self.startSudoku


class Square:
  def __init__(self):
      self.numPossible = 9
      self.numDefinite = 0
      self.numbers = [1] * 9

  def getnumPossible(self):
      return self.numPossible

  def getnumDefinite(self):
      return self.numDefinite

  def setnumDefinite(self, num):
      if num > 0:
          for i in range(9):
              if i == num - 1:
                  self.numbers[i] = 1
              else:
                  self.numbers[i] = 0
          self.updateSquare()

  def updateSquare(self):
      self.numPossible = sum(self.numbers)
      if self.numPossible == 1:
          self.numDefinite = self.numbers.index(1) + 1
      elif self.numPossible == 0:
          self.numDefinite = 0

  def setNumImPos(self, num):
      self.numbers[num - 1] = 0

  def choseNum(self, num):
      x = 0
      for i in range(9):
          if self.numbers[i] == 1:
              if x == num:
                  return i + 1
              else:
                  x += 1


class Grid:
  def __init__(self):
      self.grid = [[Square() for j in range(9)] for i in range(9)]

  def logicUpdate(self):
      madeAChange = False
      changeMadeInIteration = True
      while changeMadeInIteration:
          changeMadeInIteration = False
          for row in range(9):
              for column in range(9):
                  if self.grid[row][column].getnumPossible() == 1:
                      num = self.grid[row][column].getnumDefinite()
                      if self.updateColumn(column, num) or self.updateRow(row, num) or self.updateAndFindBlock(row, column, num):
                          changeMadeInIteration = True
          self.updateGrid()
          if changeMadeInIteration:
              madeAChange = True
      return madeAChange

  def isFinished(self):
      return all(self.grid[row][column].getnumPossible() == 1 for row in range(9) for column in range(9))

  def SetSquare(self, row, column, input):
      self.grid[row][column].setnumDefinite(input)

  def updateColumn(self, column, num):
      madeAChange = False
      for row in range(9):
          if self.grid[row][column].getnumPossible() > 1:
              if self.grid[row][column].getNumImPos(num) == 1:
                  madeAChange = True
                  self.grid[row][column].setNumImPos(num)
                  self.grid[row][column].updateSquare()
      return madeAChange

  def updateRow(self, row, num):
      madeAChange = False
      for column in range(9):
          if self.grid[row][column].getnumPossible() > 1:
              if self.grid[row][column].getNumImPos(num) == 1:
                  madeAChange = True
                  self.grid[row][column].setNumImPos(num)
                  self.grid[row][column].updateSquare()
      return madeAChange

  def updateBlock(self, num, location):
      madeAChange = False
      x, y = ((0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6))[location - 1]
      for xOrigin in range(3):
          for yOrigin in range(3):
              if self.grid[x + xOrigin][y + yOrigin].getnumPossible() > 1:
                  if self.grid[x + xOrigin][y + yOrigin].getNumImPos(num) == 1:
                      madeAChange = True
                      self.grid[x + xOrigin][y + yOrigin].setNumImPos(num)
                      self.grid[x + xOrigin][y + yOrigin].updateSquare()
      return madeAChange

  def updateAndFindBlock(self, row, column, num):
      madeAChange = False
      location = (column // 3) * 3 + (row // 3) + 1
      return self.updateBlock(num, location)

  def Outputgrid(self):
      for row in range(9):
          print(''.join(str(self.grid[row][column].getnumDefinite()) for column in range(9)))

  def updateGrid(self):
      for row in range(9):
          for column in range(9):
              self.grid[row][column].updateSquare()

  def HowManyChildren(self):
      numOfKids = 9
      for row in range(9):
          for column in range(9):
              if numOfKids > self.grid[row][column].getnumPossible():
                  if self.grid[row][column].getnumPossible() > 1:
                      numOfKids = self.grid[row][column].getnumPossible()
      return numOfKids

  def findChild(self, num, numofchildren):
      childgrid = Grid()
      for row in range(9):
          for column in range(9):
              if self.grid[row][column].getnumPossible() == numofchildren:
                  x = self.grid[row][column].choseNum(num)
                  childgrid.grid[row][column].setnumDefinite(x)
                  return childgrid

  def isComplete(self):
      return all(self.grid[row][column].getnumPossible() == 1 for row in range(9) for column in range(9))


stack1 = gridStack()
stack2 = gridStack()
sudoku = [[2, 6, 7, 8, 1, 5, 0, 0, 9],
        [3, 4, 1, 6, 2, 9, 5, 0, 0],
        [5, 8, 9, 4, 7, 3, 2, 1, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 2, 0, 0, 7, 6, 0, 0],
        [0, 0, 3, 0, 6, 2, 7, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 4, 0, 8, 6, 1, 0, 2],
        [0, 0, 6, 0, 5, 0, 8, 0, 3]]

grid = Grid()
checkNextGridStack = stack1
VisitedGridStack = stack2
treeSearch = treeSearch(grid, checkNextGridStack, VisitedGridStack, sudoku)
grid = treeSearch.doDFS()

print(" ")
print("Solved Sudoku Grid:")
grid.Outputgrid()
