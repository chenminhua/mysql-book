#include "util.h"

// MAX-HEAPIFY(A,i)
//     l <- LEFT(i)
//     r <- RIGHT(i)
//     if l <= heap-size[A] and A[l]>A[i]
//         then largest <- l
//         else largest <- i
//     if r <= heap-size[A] and A[r] > A[largest]
//         then largest <-r
//     if largest != i
//         then exchange A[i] <-> A[largest]
//             MAX-HEAPIFY(A, largest)
void max_heapify(int *arr, int i, int size)
{
    int l, r;
    l = 2 * i + 1;
    r = 2 * i + 2;
    if (l <= size)
    {
        int largest, temp;
        if (l < size && arr[l] > arr[i])
        {
            largest = l;
        }
        else
        {
            largest = i;
        }

        if (r < size && arr[r] > arr[largest])
        {
            largest = r;
        }

        if (largest != i)
        {
            temp = arr[i];
            arr[i] = arr[largest];
            arr[largest] = temp;
            max_heapify(arr, largest, size);
        }
    }
}

// BUILD-MAX-HEAP(A)
//     heap-size[A] <- length(A)
//     for i <- [length[A]/2] downto 1
//         do MAX-HEAPIFY(A, i)
void build_heap(int *arr, int size)
{
    int i;
    for (i = (size + 1) / 2; i >= 0; i--)
    {
        max_heapify(arr, i, size);
    }
}

int main()
{
    int *arr = generateArr(10);
    build_heap(arr, 10);
    printArr(arr, 10);
}