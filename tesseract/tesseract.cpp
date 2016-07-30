#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>

#define SRC_PATH argv[1]
#define DES_PATH argv[2]

int main(int argc, char* argv[])
{
	int ret = 0;

	if(argc < 3)
	{
		printf("Usage: ./demo_tesseract src_path des_path\n");
		return -1;
	}

	printf("src_path: %s\n", SRC_PATH);
	printf("dec_path: %s\n", DES_PATH);

	char* outText;

	tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();

	//Initialize tesseract-ocr with English
	if(api->Init(NULL, "eng"))
	{
		fprintf(stderr, "Could not initialize tesseract.\n");
		return -1;
	}

	//Open input image with leptonica lib
	Pix* image = pixRead(SRC_PATH);
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

	return 0;
}
