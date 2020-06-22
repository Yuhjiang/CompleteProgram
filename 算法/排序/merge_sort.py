import random


def merge_sort(list_):
    copy_buffer = list_[:]
    merge_sort_helper(list_, copy_buffer, 0, len(list_)-1)


def merge_sort_helper(list_, copy_buffer, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort_helper(list_, copy_buffer, left, mid)
        merge_sort_helper(list_, copy_buffer, mid+1, right)
        merge(list_, copy_buffer, left, mid, right)


def merge(list_, copy_buffer, left, mid, right):
    l1 = left
    l2 = mid + 1

    for i in range(left, right+1):
        if l1 > mid:
            copy_buffer[i] = list_[l2]
            l2 += 1
        elif l2 > right:
            copy_buffer[i] = list_[l1]
            l1 += 1
        elif list_[l1] < list_[l2]:
            copy_buffer[i] = list_[l1]
            l1 += 1
        else:
            copy_buffer[i] = list_[l2]
            l2 += 1

    for i in range(left, right+1):
        list_[i] = copy_buffer[i]


if __name__ == '__main__':
    l = list(range(10))
    random.shuffle(l)
    merge_sort(l)
    print(l)