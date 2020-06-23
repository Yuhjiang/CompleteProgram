import random


def insertion_sort(list_):
    for i in range(1, len(list_)):
        data_to_insert = list_[i]
        j = i - 1
        while j >= 0:
            if data_to_insert < list_[j]:
                list_[j+1] = list_[j]
                j -= 1
            else:
                break
        list_[j+1] = data_to_insert


if __name__ == '__main__':
    l = list(range(10))
    random.shuffle(l)
    insertion_sort(l)
    print(l)