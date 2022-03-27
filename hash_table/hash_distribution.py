from collections import Counter
from typing import Iterable
from string import printable

def distribute(items: list=[], num_containers: int=1, hash_function=hash)->Iterable[int]:
    return Counter([hash_function(item)%num_containers for item in items])

def plot(histogram)->None:
    for key in sorted(histogram):
        count = histogram[key]
        padding = (max(histogram.values()) - count)*" "

        print(f"{key: 3} {'■'*count}{padding} ({count})")

if __name__=='__main__':
    my_counter = distribute(items=printable, num_containers=5)
    print(my_counter)

    plot(my_counter)

    print(hash(1))
