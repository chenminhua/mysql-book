/*************************************************************************
	> File Name: insert_sort.c
	> Author: 
	> Mail: 
	> Created Time: Wed Jun 27 18:06:15 2018
 ************************************************************************/

#include "util.h"

void insert_sort(int *arr, int size)
{
    int i, j, tmp;
    for (i = 0; i < size; i++)
    {
        j = i;
        tmp = arr[i];

        while (j > 0 && tmp < arr[j - 1])
        {
            arr[j] = arr[j - 1];
            j--;
        }
        arr[j] = tmp;
    }
}

int main()
{
    int *arr = generateArr(1000);
    insert_sort(arr, 1000);
    printArr(arr, 1000);
}
