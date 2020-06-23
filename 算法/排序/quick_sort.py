import random


def quick_sort(list_):
    quick_sort_helper(list_, 0, len(list_)-1)


def quick_sort_helper(list_, left, right):
    if left < right:
        pivot = partition(list_, left, right)
        quick_sort_helper(list_, left, pivot)
        quick_sort_helper(list_, pivot+1, right)


def partition(list_, left, right):
    middle = (left + right) // 2
    pivot = list_[middle]

    list_[right], list_[middle] = list_[middle], list_[right]
    boundary = left

    for i in range(left, right):
        if list_[i] < pivot:
            list_[boundary], list_[i] = list_[i], list_[boundary]
            boundary += 1
    list_[boundary], list_[right] = list_[right], list_[boundary]

    return boundary


if __name__ == '__main__':
    l = list(range(1))
    random.shuffle(l)
    quick_sort(l)
    print(l)