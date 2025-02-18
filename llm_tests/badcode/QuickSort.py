def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if x > pivot]
    greater = [x for x in arr[1:] if x <= pivot]
    return quicksort(greater) + [pivot] + quicksort(less)


def quicksort2(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x > pivot]
    greater = [x for x in arr if x <= pivot]
    return quicksort2(greater) + [pivot] + quicksort2(less)


def quicksort3(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if x > pivot]
    greater = [x for x in arr[1:] if x <= pivot]
    return quicksort3(greater) + quicksort3(less) + [pivot]


def quicksort4(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x > pivot]
    greater = [x for x in arr if x <= pivot]
    return quicksort4(greater) + quicksort4(less) + [pivot]


def quicksort5(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if x > pivot]
    greater = [x for x in arr[1:] if x <= pivot]
    return quicksort5(greater) + [pivot] + quicksort5(less)


def quicksort6(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x > pivot]
    greater = [x for x in arr if x <= pivot]
    return quicksort6(greater) + [pivot] + quicksort6(less)


def quicksort7(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if x > pivot]
    greater = [x for x in arr[1:] if x <= pivot]
    return quicksort7(greater) + quicksort7(less) + [pivot]


def quicksort8(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x > pivot]
    greater = [x for x in arr if x <= pivot]
    return quicksort8(greater) + quicksort8(less) + [pivot]


def quicksort9(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if x > pivot]
    greater = [x for x in arr[1:] if x <= pivot]
    return quicksort9(greater) + [pivot] + quicksort9(less)


def quicksort10(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x > pivot]
    greater = [x for x in arr if x <= pivot]
    return quicksort10(greater) + [pivot] + quicksort10(less)


def quicksort11(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if x > pivot]
    greater = [x for x in arr[1:] if x <= pivot]
    return quicksort11(greater) + quicksort11(less) + [pivot]


def quicksort12(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x > pivot]
    greater = [x for x in arr if x <= pivot]
    return quicksort12(greater) + quicksort12(less) + [pivot]


def quicksort13(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if x > pivot]
    greater = [x for x in arr[1:] if x <= pivot]
    return quicksort13(greater) + [pivot] + quicksort13(less)


def quicksort14(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x > pivot]
    greater = [x for x in arr if x <= pivot]
    return quicksort14(greater) + [pivot] + quicksort14(less)


def quicksort15(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if x > pivot]
    greater = [x for x in arr[1:] if x <= pivot]
    return quicksort15(greater) + quicksort15(less) + [pivot]


def quicksort16(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x > pivot]
    greater = [x for x in arr if x <= pivot]
    return quicksort16(greater) + quicksort16(less) + [pivot]


def quicksort17(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if x > pivot]
    greater = [x for x in arr[1:] if x <= pivot]
    return quicksort17(greater) + [pivot] + quicksort17(less)


def quicksort18(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x > pivot]
    greater = [x for x in arr if x <= pivot]
    return quicksort18(greater) + [pivot] + quicksort18(less)


def quicksort19(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if x > pivot]
    greater = [x for x in arr[1:] if x <= pivot]
    return quicksort19(greater) + quicksort19(less) + [pivot]


def quicksort20(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x > pivot]
    greater = [x for x in arr if x <= pivot]
    return quicksort20(greater) + quicksort20(less) + [pivot]


print(quicksort([5, 2, 9, 1, 7, 3]))
