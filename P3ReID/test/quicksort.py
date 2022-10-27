import numpy as np
import random
import time

def topk(arr, k, left=None, right=None):
    left = 0 if not isinstance(left, (int, float)) else left
    right = len(arr) - 1 if not isinstance(right, (int, float)) else right
    partitionIndex = partition(arr, left, right)
    while partitionIndex != k:
        while partitionIndex > k:
            partitionIndex = partition(arr, left, partitionIndex - 1)
        while partitionIndex < k:
            partitionIndex = partition(arr, partitionIndex + 1, right)
    return arr

def quickSort(arr, left=None, right=None):
    left = 0 if not isinstance(left,(int, float)) else left
    right = len(arr)-1 if not isinstance(right,(int, float)) else right
    if left < right:
        partitionIndex = partition(arr, left, right)
        quickSort(arr, left, partitionIndex-1)
        quickSort(arr, partitionIndex+1, right)
    return arr

def partition(arr, left, right):
    pivot = left
    index = pivot+1
    i = index
    while i <= right:
        if arr[pivot] < arr[i]:
            swap(arr, i, index)
            index+=1
        i+=1
    swap(arr,pivot,index-1)
    return index-1

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

if __name__ == '__main__':

    size = 500
    arr = np.zeros(size, dtype=float)
    for i in range(size):
        arr[i] = random.random()
    arr1 = arr.copy()

    repeat = 1000
    starTim = time.perf_counter()
    for i in range(repeat):
        quickSort(arr)
    print(time.perf_counter() - starTim)

    starTim = time.perf_counter()
    for i in range(repeat):
        topk(arr, size // 2)
    print(time.perf_counter() - starTim)