from random import randint
import tkinter as tk
from time import sleep

def seed(mapWidth, mapHeight, cellWidth, cellHeight):
    """ returns a new cellMap randomly populated with cells """
    # create a new map
    cellMap = []

    # populate it randomly with live and dead cells (noisy start)
    for y in range(mapHeight):
        row = []
        for x in range(mapWidth):
            row.append(randint(0, 1))
        cellMap.append(row)

    # return the map
    return cellMap


def isValidCell(x, y, mapWidth, mapHeight):
    """ returns true if x, y, is on the map, otherwise false """
    return 0 <= x < mapWidth and 0 <= y < mapHeight


def stepCell(x, y, mapWidth, mapHeight, cellMap):
    """ updates the cell at x, y according to the life values of its neighbours """
    neighbourCount = -cellMap[y][x]
    for i in range(-1, 1):
        for j in range(-1, 1):
            if isValidCell(x + i, y + j, mapWidth, mapHeight):
                neighbourCount += cellMap[y + j][x + i]

    cellMap[y][x] = 0 if neighbourCount < 3 or neighbourCount > 4 else 1


def step(cellMap, mapWidth, mapHeight):
    """ updates each cell in the map according to the life values of their neighbours """
    for y in range(mapHeight):
        for x in range(mapHeight):
            stepCell(x, y, mapWidth, mapHeight, cellMap)


def drawCells(mapWidth, mapHeight, cellWidth, cellHeight, cellMap, canvas):
    for y in range(mapHeight):
        for x in range(mapWidth):
            if cellMap[y][x] == 1:
                canvas.create_rectangle(x, y, x + cellWidth, y + cellHeight, fill='black')
            else:
                canvas.create_rectangle(x, y, x + cellWidth, y + cellHeight, fill='white')


def runSim(mapWidth=800, mapHeight=800, cellWidth=50, cellHeight=50):
    print("initializing tkinter...")
    root = tk.Tk()
    root.wm_title = ("Game of Life")

    print("generating canvas...")
    canvas = tk.Canvas(root, width = mapWidth, height = mapHeight)
    canvas.grid(row=0, column=0)

    print("generating seed...")

    cellMap = seed(mapWidth, mapHeight, cellWidth, cellHeight)

    print("starting simulation...")
    while True:
        print("deleting")
        canvas.delete("all")
        print("stepping")
        step(cellMap, mapWidth, mapHeight)
        print("drawing")
        drawCells(mapWidth, mapHeight, cellWidth, cellHeight, cellMap, canvas)
        print("updating")
        canvas.update()

    mainloop()
    root.destroy()


if __name__ == '__main__':
    runSim()
