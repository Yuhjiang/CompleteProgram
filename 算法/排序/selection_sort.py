import random


def select_sort(list_):
    for i in range(len(list_) - 1):
        min_index = i
        for j in range(i+1, len(list_)):
            if list_[j] < list_[min_index]:
                min_index = j

        list_[i], list_[min_index] = list_[min_index], list_[i]


if __name__ == '__main__':
    l = list(range(10))
    random.shuffle(l)
    select_sort(l)
    print(l)