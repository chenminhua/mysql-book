#include "util.h"

#include <stdlib.h>

int *generateArr(int size)
{
  int i;
  int *arr = new int[size];
  for (i = 0; i < size; i++)
  {
    arr[i] = rand() / 2700000;
  }
  return arr;
};

void printArr(int *arr, int size)
{
  int i;
  for (i = 0; i < size; i++)
  {
    printf("%d, ", arr[i]);
  }
  printf("\n");
}