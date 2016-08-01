#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <convert.h>
#define SRC_PATH argv[1]
#define DES_PATH argv[2]
#define OCR_TYPE argv[3]
#define OCR_TYPE_MAX_LEN 255
#define IMAGE_MAX_LEN 255

char* image_tif; 

int main(int argc, char* argv[])
{
	int ret = 0;

	if(argc < 4)
	{   
		printf("Usage: ./demo_tesseract src_path des_path ocr_type\n");
		free(image_tif);
		return -1; 
	} 

	image_tif = (char*) malloc(sizeof(char*) * IMAGE_MAX_LEN);
	if(image_tif == NULL)
	{
		fprintf(stderr, "malloc image_tif fail\n");
		return -1;
	}

	int len = strrchr(SRC_PATH, '.') - SRC_PATH;
	strncpy(image_tif, SRC_PATH, len);
	strcat(image_tif, ".tif");
	printf("%s\n", strstr(SRC_PATH, "."));
	printf("src_path: %s\n", SRC_PATH);
	printf("image_tif: %s\n", image_tif);
	printf("dec_path: %s\n", DES_PATH);
	printf("ocr_type: %s\n", OCR_TYPE);

	convert(SRC_PATH, image_tif);

	char* outText;
	char* ocr_type = (char*) malloc(sizeof(char*) * OCR_TYPE_MAX_LEN);
	if(ocr_type ==NULL)
	{
		free(image_tif);
		fprintf(stderr, "malloc ocr_type fail\n");
		return -1;
	}

	strcpy(ocr_type, OCR_TYPE);

	tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();

	//Initialize tesseract-ocr with English
	if(api->Init(NULL, ocr_type))
	{
		fprintf(stderr, "Could not initialize tesseract.\n");
		free(ocr_type);
		free(image_tif);
		return -1;
	}

	//Open input image with leptonica lib
	//	Pix* image = pixRead(SRC_PATH);
	Pix* image = pixRead(image_tif);
	api->SetImage(image);
	
	//Get ocr result
	outText = api->GetUTF8Text();
	printf("OCR output: %s.\n", outText);

	FILE* pf;

	pf = fopen(DES_PATH, "a+");
	if(pf == NULL)
	{
		fprintf(stderr, "open %s error\n", DES_PATH);
		ret = -1;
		goto ocr_finish;
	}

	fprintf(pf, "%s", outText);
	fclose(pf);

ocr_finish:
	//Destroy used obj and release memory
	api->End();
	delete[] outText;
	pixDestroy(&image);
	free(ocr_type);
	free(image_tif);

	return 0;
}
