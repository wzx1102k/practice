#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <MagickCore/MagickCore.h>
#include "demo_image.h"

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

int convert(const char* input, char* output)
{
	ExceptionInfo *exception;

	Image *image, *images, *resize_image, *thumbnails;
	ImageInfo *image_info;
	
	/*Initialize the image info structure and read an image.*/
	MagickCoreGenesis(input,MagickTrue);
	exception=AcquireExceptionInfo();
	image_info=CloneImageInfo((ImageInfo *) NULL);
	(void) strcpy(image_info->filename,input);
	images=ReadImage(image_info,exception);
	if (exception->severity != UndefinedException)
		CatchException(exception);
	if (images == (Image *) NULL)
		exit(1);
	
	/*Convert the image to a thumbnail.*/
	thumbnails=NewImageList();
	while ((image=RemoveFirstImageFromList(&images)) != (Image *) NULL)
	{
		resize_image=ResizeImage(image,106,80,LanczosFilter,exception);
		if (resize_image == (Image *) NULL)
			MagickError(exception->severity,exception->reason,exception->description);
		(void) AppendImageToList(&thumbnails,resize_image);
		DestroyImage(image);
	}
	
	/*Write the image thumbnail.*/
	(void) strcpy(thumbnails->filename,output);
	WriteImage(image_info,thumbnails, exception);
	
	/*Destroy the image thumbnail and exit.*/
	thumbnails=DestroyImageList(thumbnails);
	image_info=DestroyImageInfo(image_info);
	exception=DestroyExceptionInfo(exception);
	MagickCoreTerminus();
	return(0);
}
