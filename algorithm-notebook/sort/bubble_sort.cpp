#include "util.h"

void bubble_sort(int *arr, int size)
{
  int i, j, tmp;
  for (i = 0; i < size; i++)
  {
    for (j = size - 1; j > i; j--)
    {
      if (arr[j] < arr[j - 1])
      {
        tmp = arr[j];
        arr[j] = arr[j - 1];
        arr[j - 1] = tmp;
      }
    }
  }
}

int main()
{
  int *arr = generateArr(10000);
  bubble_sort(arr, 10000);
  printArr(arr, 10000);
}
