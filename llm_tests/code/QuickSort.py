def quicksort(arr):
    """
    Sorts an array using the QuickSort algorithm.

    Args:
        arr (list): The array to be sorted.

    Returns:
        list: The sorted array.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


# Example usage:
arr = [3, 6, 8, 10, 1, 2, 1]
print("Original array:", arr)
print("Sorted array:", quicksort(arr))
