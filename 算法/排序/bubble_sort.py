import random


def bubble_sort(list_):
    for i in range(len(list_)-1, -1, -1):
        for j in range(i):
            if list_[j+1] < list_[j]:
                list_[j+1], list_[j] = list_[j], list_[j+1]


if __name__ == '__main__':
    l = list(range(10))
    random.shuffle(l)
    bubble_sort(l)
    print(l)
