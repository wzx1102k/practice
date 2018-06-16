#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void calSum(const void* src, int row, int col, void* dst)
{
    char *sum = (char*) malloc(row);
    int sum_col = 0;

    memset(sum, 0, row);
    for(int i=0; i<col; i++)
    {
        sum_col = 0;
        for(int j=0; j<row; j++)
        {
            *(char*)(dst + col*j + i) = *(char*)(src + col*j + i) + *(sum + j) + sum_col;
            sum_col += *(char*)(src + col*j + i);
            *(sum + j) += sum_col;
        }
    }
}



int main(void)
{
    char src[3][5] = {
           0, 1, 2, 3, 4,
           5, 6, 7, 8, 9,
           1, 2, 3, 4, 5
   };

    char dst[3][5] = {0};

    calSum(&src, 3, 5, &dst);
    printf("-----------src------\n");
    for(int i=0; i<3; i++)
    {
        for(int j=0; j<5; j++)
        {
            printf("%d ", src[i][j]);
        }
        printf("\n");
    }
    printf("---------des--------\n");
    for(int i=0; i<3; i++)
    {
        for(int j=0; j<5; j++)
        {
            printf("%d ", dst[i][j]);
        }
        printf("\n");
    }
   return 0;
}
