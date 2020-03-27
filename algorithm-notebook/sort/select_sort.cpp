#include "util.h"

// 每次都找最小的一个，并把它放到最前面
void select_sort(int *arr, int size)
{
  int i, j, temp, minIndex;
  for (i = 0; i < size; i++)
  {
    minIndex = i;
    for (j = i + 1; j < size; j++)
      if (arr[j] < arr[minIndex])
        minIndex = j;
    if (minIndex != i)
    {
      temp = arr[i];
      arr[i] = arr[minIndex];
      arr[minIndex] = temp;
    }
  }
}

int main()
{
  int *arr = generateArr(10000);
  select_sort(arr, 10000);
  printArr(arr, 10000);
}
