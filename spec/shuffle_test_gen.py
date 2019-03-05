import binascii
import csv
import random
from hashlib import sha256
import yaml

SHUFFLE_ROUND_COUNT = 90


def bytes_to_int(data: bytes) -> int:
    return int.from_bytes(data, 'little')


def int_to_bytes1(x):
    return x.to_bytes(1, 'little')


def int_to_bytes4(x):
    return x.to_bytes(4, 'little')


def hash(data: bytes) -> bytes:
    return sha256(data).digest()


def get_permuted_index(index: int, list_size: int, seed: bytes) -> int:
    """
    Return `p(index)` in a pseudorandom permutation `p` of `0...list_size-1` with ``seed`` as entropy.

    Utilizes 'swap or not' shuffling found in
    https://link.springer.com/content/pdf/10.1007%2F978-3-642-32009-5_1.pdf
    See the 'generalized domain' algorithm on page 3.
    """
    assert index < list_size
    assert list_size <= 2 ** 40

    for round in range(SHUFFLE_ROUND_COUNT):
        pivot = bytes_to_int(hash(seed + int_to_bytes1(round))[0:8]) % list_size
        flip = (pivot - index) % list_size
        position = max(index, flip)
        source = hash(seed + int_to_bytes1(round) + int_to_bytes4(position // 256))
        byte = source[(position % 256) // 8]
        bit = (byte >> (position % 8)) % 2
        index = flip if bit else index

    return index

   

# runs new shuffling algorithm
def shuffle_indexes(idxs, seed):
    list_size = len(idxs)
    shuffling = [0 for _ in range(list_size)]
    for i in range(list_size):
        shuffling[get_permuted_index(i, list_size, seed)] = i
    return [idxs[x] for x in shuffling]
  

# gen_test_outputs reads shuffle.yaml locally file then writes the outputs of new_shuffle_algorithm to it.
def gen_test_outputs(yaml_path = "/home/ai/shuffle.yaml"):
    with open(yaml_path, 'r') as f:
        shuffle = yaml.load(f.read())
    for idx, test in enumerate(shuffle['test_cases']):
        if 'input' in test:
            shuffle['test_cases'][idx]['output'] = shuffle_indexes(test['input'], test['seed'])
    with open(yaml_path, 'w') as f:
        yaml.dump(shuffle, f)

