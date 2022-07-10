from multiprocessing import Condition, Process
from time import sleep



def task(condition: Condition=None)->None:
    sleep(2)

    print("Child process sending notification...")
    with condition:
        condition.notify()

    # Do something else
    sleep(1)

if __name__=="__main__":
    # Create a new condition variable
    condition = Condition()

    print("Main process waiting for data...")
    with condition:
        worker = Process(target=task, args=(condition,))
        worker.start()

        condition.wait()

    print("Main process all done")
