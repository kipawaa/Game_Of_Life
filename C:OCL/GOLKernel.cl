__kernel void computeLifeValues(__global int** cellMap, __global int height, __global int width) {
	int idx = get_global_id(0);
	surroundingLifeCount = 0;
	//TODO: this doesn't reject counting values past the edges
	surroundingLifeCount += *(cellMap + idx - 1) + *(cellMap + idx + 1); // counts the values of the cells left and right of the cell of interest (COI))
	surroundingLifeCount += *(cellMap + idx - width - 1) + *(cellMap + idx - width) + *(cellMap + idx - width + 1); // counts the values of the cells above the COI
	surroundingLifeCount += *(cellMap + idx + width - 1) + *(cellMap + idx + width) + *(cellMap + idx + width + 1); // counts the values of the cells below the COI
	
	// sets the value of the cell based on the default rules of Conway's GOL
	*(cellMap + idx) = 0 * (surroundingLifeCount < 3) + (surroundingLifeCount == 3) + 0 * (surroundingLifeCount > 4);
}
