// much of this code is branchless. If you're confused, check out https://www.youtube.com/watch?v=bVJ-mWWL7cE&list=WL&index=15&t=676s or my examples @ https://github.com/kipawaa/Little-Projects/blob/master/C/branchless.c
__kernel void computeLifeValues(__global int* cellMap, __global int* height, __global int* width) {
	// cellMap is a 2d array with 0 for a dead cell and 1 for a live cell, width and height are the dimensions of cellMap
	
	// get thread index which will be used to calculate a cell at the same index
	int idx = get_global_id(0);

	// set the number of living cells around it to default at 0
	int surroundingLifeCount = 0;

	// (*(cellMap + idx) % width == 0)		true if the COI (cell of interest) is at the left edge of the map
	// (*(cellMap + idx) % width == width - 1)	true if the COI is at the right edge of the map
	// (idx / width == 0)				true if the COI is at the top edge of the map
	// (idx / width == height)			true if the COI is at the bottom edge of the map
	
	// determine which cells around it are applicable and alive
	// TODO one of these isn't indexing properly, must be fixed
	surroundingLifeCount += !(*(cellMap + idx) % *(width) == 0) * // conditional for left side (ensures there is a cell to the left)
				(*(cellMap + idx - 1)); // value of the cell to the left
	surroundingLifeCount += !(*(cellMap + idx) % *(width) == *(width) - 1) * // conditional for the right side
				(*(cellMap + idx + 1)); // value of the cell to the right
	surroundingLifeCount += !(*(cellMap + idx) % *(width) == 0) * // conditional for the left
				!(idx / *(width) == 0) * // conditional for the cell above
				(*(cellMap + idx - *(width) - 1)); // value of the cell above and to the left
	surroundingLifeCount += !(idx / *(width) == 0) * // conditional for above
				(*(cellMap + idx - *(width))); // value of the cell above
	surroundingLifeCount += !(*(cellMap + idx) % *(width) == *(width) - 1) * // conditional for the right
				!(idx / *(width) == 0) * // conditional for above
				(*(cellMap + idx - *(width) + 1)); // value of the cell above and to the right
	surroundingLifeCount += !(*(cellMap + idx) % *(width) == 0) * // conditional for the left
				!(idx / *(width) == *(height)) * // conditional for below
				(*(cellMap + idx + *(width) - 1)); // value of the cell below and to the left
	surroundingLifeCount += !(idx / *(width) == *(height)) * // conditional for below
				(*(cellMap + idx + *(width))); // value of the cell below
	surroundingLifeCount += !(*(cellMap + idx) % *(width) == *(width) - 1) * // conditional for the right
				!(idx / *(width) == *(height)) * // conditional for below
				(*(cellMap + idx + *(width) + 1)); // value of the cell below and to the right
	
	// set the value of the cell based on the default rules of Conway's GOL 
	if (*(cellMap + idx) && (surroundingLifeCount == 2 || surroundingLifeCount == 3)) {
		*(cellMap + idx) = 1;
	} else if (!*(cellMap + idx) && surroundingLifeCount == 3) {
		*(cellMap + idx) = 1;
	} else {
		*(cellMap + idx) = 0;
	}
}
