"""
迭代器模式
https://refactoringguru.cn/design-patterns/iterator/python/example
"""
from collections.abc import Iterable, Iterator
from typing import Any, List


class WordsCollection(Iterable):
    def __init__(self, collection: List[Any] = None) -> None:
        if not collection:
            self._collection = []
        else:
            self._collection = collection

    def __iter__(self):
        return AlphabeticalOrderIterator(self._collection)

    def get_reverse_iterator(self):
        return AlphabeticalOrderIterator(self._collection, True)

    def add_item(self, item: Any):
        self._collection.append(item)


class AlphabeticalOrderIterator(Iterator):
    _position: int = None
    _reverse: bool = False

    def __init__(self, collection: List[Any], reverse: bool = True) -> None:
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()
        return value


if __name__ == '__main__':
    collection = WordsCollection()
    collection.add_item('First')
    collection.add_item('Second')
    collection.add_item('Third')

    # print('Straight traversal:')
    # print('\n'.join(collection))
    # print('\n')

    print('Reverse traversal:')
    print('\n'.join(collection.get_reverse_iterator()))