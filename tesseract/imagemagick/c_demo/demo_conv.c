#include <stdio.h>
#include "convert.h"
#include <stdlib.h>
#include <time.h>

int main(int argc,char **argv)
{
	if (argc != 3)
	{   
		(void) fprintf(stdout,"Usage: %s image thumbnail\n",argv[0]);
		exit(0);
	}   

	convert(argv[1], argv[2]);
	return 0;
}

