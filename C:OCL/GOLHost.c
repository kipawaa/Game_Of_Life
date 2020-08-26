#include<stdio.h>
#include<stdlib.h>

#ifdef __APPLE__
	#include<OpenCL/opencl.h>
#else
	#include<CL/cl.h>
#endif

// used to print the map (remove once a better display solution has been found)
void printArr(int* map, int width, int height) {
	for (int i = 0; i < width * height; i++) {
		if (map[i]) printf("[]");
		else printf("  ");
		if (!(i % width)) printf("\n");
	}
	printf("\n");
}

int main() {
	int width;
	int height;
	printf("input the desired map width: ");
	scanf("%d", &width);

	printf("input the desired map height: ");
	scanf("%d", &height);

	// allocate memory for the map (OpenCL kernels don't seem to be able to handle 2D arrays, so this is one dimensional)
	int* cellMap = (int*) malloc(width * height * sizeof(int));

	// randomize the values in the map in range (0, 1)
	for (int i = 0; i < width * height; i++) {
		cellMap[i] = rand() % 2; // rand returns large integers, adding "% 2" envenly distributes 1s and 0s
	}
	printArr(cellMap, width, height);

	// maximum size of the OCL file to be used
	const size_t clFileSize = 0x100000;

	// string to store the code copied from the OCL file
	char* clSource = (char*) malloc(clFileSize);

	// open the .cl file containing the OCL code and copy it to the clSource string, then close the file
	FILE* clFile = fopen("GOLKernel.cl", "r");
	fread(clSource, 1, clFileSize, clFile);
	fclose(clFile);

	// platform and device information
	cl_platform_id platform = NULL;
	cl_uint numPlatforms;

	cl_device_id device = NULL;
	cl_uint numDevices;
	
	// stores errors and other return values from OCL functions
	cl_int ret;

	// automatically find and store an available platform in the platform variable
	ret = clGetPlatformIDs(1, &platform, &numPlatforms);
	if (ret) {
		printf("platform: %d\n", ret);
		return ret;
	}

	// automatically find and store an available device that runs on the current platform in the device variable
	ret = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, &numDevices);
	if(ret) {
		printf("device: %d\n", ret);
		return ret;
	}

	// create a context
	cl_context context = clCreateContext(NULL, 1, &device, NULL, NULL, &ret);
	if (ret) {
		printf("context: %d\n", ret);
		return ret;
	}

	// create command queue
	cl_command_queue queue = clCreateCommandQueue(context, device, 0, &ret);
	if (ret) {
		printf("queue: %d\n", ret);
		return ret;
	}

	// create buffers for data that will be passed to the compute device
	cl_mem width_obj = clCreateBuffer(context, CL_MEM_READ_ONLY, sizeof(int), NULL, &ret);
	cl_mem height_obj = clCreateBuffer(context, CL_MEM_READ_ONLY, sizeof(int), NULL, &ret);
	cl_mem map_obj = clCreateBuffer(context, CL_MEM_WRITE_ONLY, width * height * sizeof(int), NULL, &ret);
	if (ret) {
		printf("buffers: %d\n", ret);
		return ret;
	}

	// get the program from the string it's stored in
	cl_program program = clCreateProgramWithSource(context, 1, (const char**)&clSource, &clFileSize, &ret);
	if (ret) {
		printf("program: %d\n", ret);
		return ret;
	}

	// now finished with the kernel source code, release the memory associated with it
	free(clSource);

	// compile the program
	ret = clBuildProgram(program, 1, &device, NULL, NULL, NULL);
	if (ret) {
		printf("build: %d\n", ret);
		return ret;
	}
	// print build errors if they occurred (this is larger than other error catches since it prints the compiling errors for the kernel)
	if (ret) {
		size_t logSize;
		clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, 0, NULL, &logSize);

		char* log = (char*)malloc(logSize);
		clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, logSize, log, NULL);
		printf("%s\n", log);
	}

	// create the kernel
	cl_kernel kernel = clCreateKernel(program, "computeLifeValues", &ret);
	if (ret) {
		printf("kernel: %d\n", ret);
		return ret;
	}

	// determine how many generations the user would like to see
	printf("enter the number of generations you'd like to observe (recommended 1000): ");
	int numGenerations = 0;
	scanf("%d", &numGenerations);
	


	// this loop runs the simulation for numGenerations generations
	for (int i = 0; i < numGenerations; i++) {
		// write the data to the buffers
		ret = clEnqueueWriteBuffer(queue, width_obj, CL_TRUE, 0, sizeof(int), &width, 0, NULL, NULL);
		ret = clEnqueueWriteBuffer(queue, height_obj, CL_TRUE, 0, sizeof(int), &height, 0, NULL, NULL);
		ret = clEnqueueWriteBuffer(queue, map_obj, CL_TRUE, 0, width * height * sizeof(int), cellMap, 0, NULL, NULL);

		// set kernel arguments
		ret = clSetKernelArg(kernel, 0, sizeof(cl_mem), (void*)&map_obj);
		ret = clSetKernelArg(kernel, 1, sizeof(cl_mem), (void*)&width_obj);
		ret = clSetKernelArg(kernel, 2, sizeof(cl_mem), (void*)&height_obj);

		// declare work group and unit sizes
		const size_t globalSize = width * height;
		const size_t localSize = 1;

		// execute the kernel
		ret = clEnqueueNDRangeKernel(queue, kernel, 1, NULL, &globalSize, &localSize, 0, NULL, NULL);

		// read data from buffer
		ret = clEnqueueReadBuffer(queue, map_obj, CL_TRUE, 0, width * height * sizeof(int), cellMap, 0, NULL, NULL);

		printArr(cellMap, width, height);
	}

	// clean up everything associated with OCL
	clFinish(queue);
	clFlush(queue);
	clReleaseKernel(kernel);
	clReleaseProgram(program);
	clReleaseMemObject(map_obj);
	clReleaseMemObject(width_obj);
	clReleaseMemObject(height_obj);
	clReleaseCommandQueue(queue);
	clReleaseContext(context);

	free(cellMap);
}
