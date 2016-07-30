#include <jni.h>
#include "com_hello.h"
#include <stdio.h>
#include <pthread.h>
#include "thread_test.h"



JNIEXPORT void JNICALL Java_com_hello_DisplayHello
(JNIEnv *env, jobject obj)
{
    printf("From jni_helloworldImpl.cpp :");
	printf("Hello world ! \n");
    test();
	return;
}
