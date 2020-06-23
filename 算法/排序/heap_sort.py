import random


def perc_down(list_, p, size):
    x = list_[p]

    left_child = lambda i: i*2+1
    while left_child(p) < size:
        child = left_child(p)

        if child < size - 1 and list_[child+1] > list_[child]:
            child += 1

        if x < list_[child]:
            list_[p] = list_[child]
        else:
            break
        p = child
    list_[p] = x


def heap_sort(list_):
    for i in range(len(list_) // 2)[::-1]:
        perc_down(list_, i, len(list_))

    for s in range(len(list_))[::-1]:
        list_[s], list_[0] = list_[0], list_[s]
        perc_down(list_, 0, s)


if __name__ == '__main__':
    l = list(range(10))
    random.shuffle(l)
    heap_sort(l)
    print(l)