
import hashlib
from typing import Tuple

def hash_without_salt_on_string(item: str) -> str:
    hash = hashlib.md5(item.encode('utf-8')).hexdigest()
    return hash


def assign_set(hash_str: str, testset_split: str) -> str:
    dataset_split = None

    hash_int = int(hash_str, 16)
    hash_modulo = hash_int % 99
    if 0 <= hash_modulo < 55:
        dataset_split = 'train'
    elif 55 <= hash_modulo < 60:
        dataset_split = 'dev-0'
    elif testset_split is not None and testset_split[0] <= hash_modulo < testset_split[1]:
        dataset_split = 'test-A'
    else:
        pass

    return dataset_split


def assign_item_to_set(item: str, testset_split: Tuple[int, int] = [60, 100]) -> str:
    '''
    Assigns item to a split subset (returns 'train', 'dev-0', 'test-A'
    or None if an item is to be discarded.

    testset_split is the range for the test-A, by default [60,100] (40% of the data set)
    can be set a smaller range

    '''
    h = hash_without_salt_on_string(item)
    return assign_set(h, testset_split)

# print(assign_item_to_set('WBC'))
