from hash_distribution import plot, distribute
from string import printable

# print(printable)

def generator_func():
    num = 1
    print('First')
    yield num
    num = 2
    print('second')
    yield num
    num = 3
    print('third')
    yield num


if __name__=='__main__':
    obj = generator_func()
    assert 2 + 2 == 5, "error msg"
    print(list(generator_func()))
