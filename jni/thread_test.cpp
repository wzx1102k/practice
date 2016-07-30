#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void* thread_function (void* arg)
{
    int count = 10;
    fprintf(stderr, "child thread pid is %d\n", (int)getpid());
    while(count--)
    {
        printf("count = %d\n", count);
        sleep(1);
    }
    return NULL;
}

void test(void)
{
    pthread_t thread;
    fprintf(stderr, "main thread pid is %d\n", (int)getpid());
    pthread_create(&thread, NULL, &thread_function, NULL);  
    sleep(30);
}