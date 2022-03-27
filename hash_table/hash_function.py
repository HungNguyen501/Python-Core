from hash_distribution import distribute, plot
from string import printable

def hash_function(key):
    return sum(
        index * ord(character)
        for index, character in enumerate(repr(key).lstrip("'"), 1)
    )

if __name__=='__main__':
    # print(hash_function('a'))
    # print(hash_function(15))
    # print(hash_function('Hello i am hung'))

    plot(distribute(items=printable, num_containers=6, hash_function=hash_function))



