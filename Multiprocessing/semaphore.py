from multiprocessing import Process, Semaphore
from random import random
from time import sleep



def task(semaphore: Semaphore=None, number: int=None)->None:
    with semaphore:
        value = random()
        sleep(value)
        print(f"Process {number} got {value}")
        # print(f"Process {number} {semaphore}")


if __name__=="__main__":
    # Set number of concurent processes that can hold the semaphore
    semaphore = Semaphore(value=3)

    procs = [Process(target=task, args=(semaphore, i)) for i in range(10)]

    for proc in procs:
        proc.start()
    
    for proc in procs:
        proc.join()




