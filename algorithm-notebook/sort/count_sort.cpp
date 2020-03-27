#include "util.h"

#define LIMIT 2000

void count_sort(int *data, int size)
{
  int counts[LIMIT] = {}, i;
  int datacopy[size];
  for (i = 0; i < size; i++)
  {
    counts[data[i]]++;
    datacopy[i] = data[i];
  }
  for (i = 1; i < LIMIT; i++)
    counts[i] += counts[i - 1];
  for (i = size - 1; i >= 0; i--)
    data[--counts[datacopy[i]]] = datacopy[i];
}

int main()
{
  int size = 1000000;
  int *arr = generateArr(size);
  count_sort(arr, size);
  //printArr(arr, size);
}