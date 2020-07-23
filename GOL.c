// IMPORTS
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<time.h>


// CONSTANTS
#define map_width 234
#define map_height 73


// STRUCTURES
// Cell stucture
typedef struct Cell {
	int state;
	int lifeCount;
} Cell;

typedef Cell CellMap[map_height][map_width];


// FUNCTIONS
// Initializes a new CellMap with random values
CellMap *initializeMap(void) {
	// callocs the necessary space
	CellMap *map = NULL;
	map = (CellMap *)calloc(map_height*map_width, sizeof(Cell));

	// seeds the random number generator by using the current time
	srand(time(0));
	for (int i = 0; i < map_height; i++) {
		for (int j = 0; j < map_width; j++) {
			// sets the state of the cell randomly to 0 or 1 (the % 2 works because even or odd numbers are generated)
			map[i][j] -> state = rand() % 2;
			map[i][j] -> lifeCount = 0;
		}
	}
	return map;
}

// function to determine a cell's life count (the number of living cells around it)
int getLifeCount(CellMap *map, int x, int y) {
	int lifeCount = 0;
	for (int i = -1; i < 2; i++) {
		for (int j = -1; j < 2; j++) {
			if (!(i == 0 && j == 0)) {
				if ((0 <= x + i) && (x + i < map_height) && (0 <= y + j) && (y + j < map_width)){
					lifeCount += map[x+i][y+j] -> state;
				}
			}
		}
	}
	return lifeCount;
}

// function to update a map based on cell's life count
void updateLifeCount(CellMap *map) {
	for (int i = 0; i < map_height; i++) {
		for (int j = 0; j < map_width; j++) {
			map[i][j] -> lifeCount = getLifeCount(map, i, j);
		}
	}

}

// updates the state of each cell in map based upon its life count
void updateState(CellMap *map) {
	for (int i = 0; i < map_height; i++) {
		for (int j = 0; j < map_width; j++) {
			// normal rules: x < 3 -> dead, x = 3 -> life, x > 4 -> dead
			if (map[i][j] -> lifeCount < 2) {
				map[i][j] -> state = 0;
			} else if (map[i][j] -> lifeCount == 3) {
				map[i][j] -> state = 1;
			} else if (map[i][j] -> lifeCount > 4) {
				map[i][j] -> state = 0;
			}
		}
	}
}

// prints the contents of a cell map
void printMap(CellMap *map) {
	printf("\n");
	for (int i = 0; i < map_height; i++) {
		for (int j = 0; j < map_width; j++) {
			if (map[i][j] -> state) printf("[]");
			else printf("  ");
		}
		printf("\n");
	}
	printf("\n");
}

// allows delaying of each print
void delay(int milliseconds) {
	clock_t start = clock();

	while (clock() < start + milliseconds);
}

int main() {
	// creates a new CellMap
	CellMap *map = initializeMap();
	
	int user = 1;
	while (user == 1) {
		// Updates the life count for each cell in map
		updateLifeCount(map);
	
		// updates the state of each cell in map
		updateState(map);
	
		// prints the map
		printMap(map);

		// delays the next print (recommended 333333)
		// delay(333333);
		delay(50000);
	}

	free(map);
}
