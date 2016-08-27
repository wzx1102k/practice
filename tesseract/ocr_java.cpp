#include <jni.h>
#include "com_ocr_java.h"
#include "ocr_tesseract.h"

JNIEXPORT jstring JNICALL Java_com_ocr_1java_OcrTesseract
        (JNIEnv * env, jobject obj, jstring srcImg, jstring desImg, jstring ocr_type) {
    const char* input = env->GetStringUTFChars(srcImg, 0);
    const char* output = env->GetStringUTFChars(desImg, 0);
    const char* type = env->GetStringUTFChars(ocr_type, 0);
    char* buf;
    printf("input: %s\n", input);
    printf("output: %s\n", output);
    printf("type: %s\n", type);

    buf = ocr_tesseract(input, output, type);

    env->ReleaseStringUTFChars(srcImg, input);
    env->ReleaseStringUTFChars(desImg, output);
    env->ReleaseStringUTFChars(ocr_type, type);
    return env->NewStringUTF(buf);
}
