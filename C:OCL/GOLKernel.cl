// much of this code is branchless. If you're confused, check out https://www.youtube.com/watch?v=bVJ-mWWL7cE&list=WL&index=15&t=676s or my examples @ https://github.com/kipawaa/Little-Projects/blob/master/C/branchless.c
__kernel void computeLifeValues(__global int** cellMap, __global int height, __global int width) {
	// cellMap is a 2d array with 0 for a dead cell and 1 for a live cell, width and height are the dimensions of cellMap
	
	// get thread index which will be used to calculate a cell at the same index
	int idx = get_global_id(0);

	// set the number of living cells around it to default at 0
	surroundingLifeCount = 0;

	// (*(cellMap + idx) % width == 0)		true if the COI (cell of interest) is at the left edge of the map
	// (*(cellMap + idx) % width == width - 1)	true if the COI is at the right edge of the map
	// (idx / width == 0)				true if the COI is at the top edge of the map
	// (idx / width == height)			true if the COI is at the bottom edge of the map
	
	// determine which cells around it are applicable and alive
	surroundingLifeCount += !(*(cellMap + idx) % width == 0) * (*(cellMap + idx - 1)); // counts the value to the left of the COI if the COI is not against the left wall
	surroundingLifecount += !(*(cellMap + idx) % width == width - 1) * (*(cellMap + idx + 1)); // counts value to the right if the COI is not against the right wall
	surroundingLifeCount += !(*(cellMap + idx) % width == 0) * !(idx / width == 0) * (*(cellMap + idx - width - 1)); // up and left
	surroundingLifeCount += !(idx / width == 0) * (*(cellMap + idx - width)); // up
	surroundingLifeCount += !(*(cellMap + idx) % width == width - 1) * !(idx / width == 0) * (*(cellMap + idx - width + 1)); // up and right
	surroundingLifeCount += !(*(cellMap + idx) % width == 0) * !(idx / width == height) * (*(cellMap + idx + width - 1)); // down and left
	surroundingLifecount += !(idx / width == height) * (*(cellMap + idx + width)); // down
	surroundingLifeCount += !(*(cellMap + idx % width == width - 1) * !(idx / width == height) * (*(cellMap + idx + width + 1)); // down and right
	
	// set the value of the cell based on the default rules of Conway's GOL 
	*(cellMap + idx) = 0 * (surroundingLifeCount < 3) + (surroundingLifeCount == 3) + 0 * (surroundingLifeCount > 4);
}
