from random import randint
import tkinter as tk

class Cell:
	def __init__(self, x, y, width, height, life):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.life = life
	
	def updateLife(self, cellMap):
		lifeCount = 0
		for i in range(-1, 1):
			for j in range(-1, 1):
				if (0 <= self.x + i and self.x + i < len(cellMap[0]) and 0 <= self.y + j and self.y + j < len(cellMap)):
					lifeCount += cellMap[self.x + i][self.y + j].life
		
		lifeCount -= self.life
		
		if lifeCount < 3:
			self.life = 0
		elif lifeCount == 3:
			self.life = 1
		elif lifeCount > 4:
			self.life = 0
	
	def draw(self, canvas):
		canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill="white")

def startMap(mapWidth, mapHeight, cellWidth, cellHeight):
	cellMap = []
	for y in range(mapHeight // cellHeight):
		row = []
		for x in range(mapWidth // cellWidth):
			row.append(Cell(x * cellWidth, y * cellHeight, cellWidth, cellHeight, randint(0, 1)))
		cellMap.append(row)
	return cellMap

def step(cellMap):
	for row in cellMap:
		for cell in row:
			cell.updateLife(cellMap);

def drawCells(cellMap, canvas):
	for row in cellMap:
		for cell in row:
			cell.draw(canvas)

def runSim(mapWidth=1920, mapHeight=1080, cellWidth=10, cellHeight=10):
	root = tk.Tk()
	root.wm_title = ("Game of Life")

	canvas = tk.Canvas(root, width = mapWidth, height = mapHeight) 
	canvas.grid(row=0, column=0)

	cellMap = startMap(mapWidth, mapHeight, cellWidth, cellHeight)
	
	while True:
		canvas.delete("all")
		step(cellMap)
		drawCells(cellMap, canvas)
		canvas.update()
	
	mainloop()
	root.destroy()

if __name__ == '__main__':
	runSim()
