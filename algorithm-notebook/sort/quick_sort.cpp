#include "util.h"
#include <assert.h>

// ```
// QUICKSORT(A, p, r)
// if p < r
//     then q <- PARTION(A, p, r)
//         QUICKSORT(A, p, q-1)
//         QUICKSORT(A, q+1, r)

// PARTITION(A, p, r)
// x <- A[r]
// i <- p
// for j <- p to r-1
//     do if A[j] <= x
//         then i <- i+1
//             exchange A[i] <-> A[j]
// exchange A[i+1] <-> A[r]
// return i+1
// ```

int partition(int *arr, int p, int r)
{
  // 将最后一个数作为分隔点，遇到小于等于分隔点的数就交换到前面去
  int x = arr[r];
  // 注意这里的i,最开始的时候可能是-1
  assert(p >= 0);
  int i = p - 1;
  int j, temp;
  for (j = p; j < r; j++)
  {
    if (arr[j] <= x)
    {
      i = i + 1;
      temp = arr[i];
      arr[i] = arr[j];
      arr[j] = temp;
    }
  }
  temp = arr[i + 1];
  arr[i + 1] = arr[r];
  arr[r] = temp;
  return i + 1;
}

void quick_sort(int *arr, int p, int r)
{
  int q;
  if (p < r)
  {
    q = partition(arr, p, r);
    // 编译器应该是有尾递归优化的
    quick_sort(arr, p, q - 1);
    quick_sort(arr, q + 1, r);
  }
}

int main()
{
  int size = 1000000;
  int *arr = generateArr(size);
  quick_sort(arr, 0, size - 1);
  //printArr(arr, size);
}