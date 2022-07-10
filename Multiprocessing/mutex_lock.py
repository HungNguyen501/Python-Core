from threading import Thread, Lock as t_lock
from multiprocessing import Process, Lock as p_lock, RLock, Value
from random import random
from time import sleep, time



def increment(lock=None, n_times: int=None, x_v=None)->None:
    """Task for thread that calls increment function n_time times

    Parameters
    lock(Lock): Lock of threading
    n_times(int): number of time is called
    """
    if isinstance(lock, type(t_lock())):
        global x

        # Use with statement, we do not need to use acquire and release for lock
        with lock:
            for _ in range(n_times):
                # Get lock
                # lock.acquire()

                x+=1

                # Release lock
                # lock.release()
    elif isinstance(lock, type(p_lock())):
        with lock:
            for _ in range(n_times):
                x_v.value+=1

def test_threading()->None:
    global x
    # Create a lock
    lock = t_lock()
  
    # Create threads
    li_threads = [Thread(target=increment, args=(lock, 1000000)) for _ in range(5)]
  
    # Start threads
    for thread in li_threads:
        thread.start()
  
    # Wait until threads finish their job
    for thread in li_threads:
        thread.join()

    print(f"x={x}")

# Use the Reentrant Lock
# If a non-reentrant lock, e.g. a multiprocessing.
# Lock was used instead, then the process would block forever waiting for the lock to become available, 
# which it can’t because the process already holds the lock.
def report(lock :RLock=None, proc_name: str=None)->None:
    with lock:
        print(f"{proc_name} done")

def process_task1(lock, proc_name: str=None, value: int=None)->None:
    with lock:
        print(f"{proc_name}: got the lock, sleeping for {value}")
        sleep(value)

        if isinstance(lock, type(RLock())):
            report(lock, proc_name)

def test_process1(lock)->None:
    # Create processes
    li_procs = [Process(target=process_task1, args=(lock, f"process_{_}", random())) for _ in range(10)]

    # Start processes
    for proc in li_procs:
        proc.start()

    # Wait for all processes to finish
    for proc in li_procs:
        proc.join()

# When we use multiprocessing in multi processes
# They won't be sharing the same globals
# This below is solution by using Vale and Array in multiprocessing
def test_process2()->None:
    x = Value("i", 0)
    # Create a lock
    lock = p_lock()
  
    # Create threads
    li_procs = [Process(target=increment, args=(lock, 1000000, x)) for _ in range(5)]
  
    # Start processes
    for proc in li_procs:
        proc.start()

    # Wait for all processes to finish
    for proc in li_procs:
        proc.join()

    print(f"x={x.value}")            


if __name__ == "__main__":
    # global variable x
    x = 0

    """Test threading
    """
    start_time = time()
    
    # test_threading()
   
    print(f"time={time() - start_time: .2f}")


    """Test multiprocessing
    """
    start_time = time()
    
    # lock = RLock()
    # test_process1(lock)

    test_process2()

    print(f"time={time() - start_time: .2f}")

