import numpy as np
import pygame

def gen_one(width, height):
    print('creating...')
    ''' returns an array of size width x height of randomly generated ones and zeroes'''
    return np.random.randint(0, 2, (width, height))


def valid_cell(arr, x, y):
    width, height = arr.shape

    return 0 <= x < width and 0 <= y < height


def surrounding_cells(arr, x, y):
    total = -arr[x, y]
    for i in range(-1, 2):
        for j in range(-1, 2):
            if valid_cell(arr, x+i, y+j):
                total += arr[x+i, y+j]
    return total


def next_gen(arr):
    width, height = arr.shape

    cells = np.zeros((width, height))
    
    for x in range(width):
        for y in range(height):

            local_population = surrounding_cells(arr, x, y)

            if local_population < 2 or local_population > 3:
                cells[x, y] = 0
            elif local_population == 3:
                cells[x, y] = 1
            else:
                cells[x, y] = arr[x, y]
    return cells


def normalize(arr):
    ''' normalizes array values from 0-255 for colouring '''
    return ((arr - arr.min()) / arr.max() * 255).astype(np.uint8)


def update_screen(arr, display):
    arr_width, arr_height = arr.shape

    display_width, display_height = pygame.display.get_surface().get_size()
    
    for i in range(arr_width):
        for j in range(arr_height):
            colour = arr[i, j]*255
            pygame.draw.rect(display, (colour, colour, colour), (i * display_width / arr_width, j * display_height / arr_height, display_width / arr_width, display_height / arr_height))
    pygame.display.flip()
    

if __name__ == '__main__':
    width = 200
    height = 200
    cells = gen_one(width, height)
    
    pygame.init()
    
    display = pygame.display.set_mode((width*4, height*4))

    clock = pygame.time.Clock()
    running=True
    
    while running:
        clock.tick(1)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        
        update_screen(cells, display)
        cells = next_gen(cells)
    
    pygame.quit()
        
        
