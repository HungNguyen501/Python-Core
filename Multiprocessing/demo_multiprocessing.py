from multiprocessing import Pool
import multiprocessing
import time

def task(arg):
    index = arg[0]
    n = arg[1]
    # time.sleep(sleep_time)
    for i in range(n):
        count = 0
        while count < 10000000:
            count += 1
        print(f"task{index}: {i+1}")
        time.sleep(1)
    print(f"task{index} is done")

def sum_nums(args):
    low = int(args[0])
    high = int(args[1])
    return sum(range(low,high+1))

def demo_multiprocessing1(n):
    """Return sum of array of numbers
    using multi-processing by method 1
    """
    procs = 3

    sizeSegment = n/procs

    # Create size segments list
    jobs = []
    for i in range(0, procs):
        jobs.append((i*sizeSegment+1, (i+1)*sizeSegment))

    pool = Pool(procs).map(sum_nums, jobs)    
    result = sum(pool)

    print(pool)
    print(result)
    print(f"number of cpus: {multiprocessing.cpu_count()}")

 
def demo_multiprocessing2(n):
    """Return sum of array of numbers
    using multi-processing by method 2
    """
    pool = Pool(4)
    r = range(0,10**8+1,n)
         # 0 at the beginning, end 100,000,000, step n of 10,000. That result is 0,10000,20000,30000 ......
    results = []
    for j in zip([x+1 for x in r],r[1:]):
                # X + 1 for x in r results 1,10001,20001,30001 ......
                # R [1:] 10000,20000,30000,40000 ...... result of a number less than the above
                # With zip function, the result of (1,10000), (10001,20000), (20001,30000) ...... 
                # same as the shortest length of the list of objects, i.e., the r [1:] the same number
                #  This put the # 1-100000000 segments.
        s = pool.apply_async(sum_nums,list(j))
                # Here is a tuple j, j fill it directly apply_async brackets on the line
                # Results obtained here is 
                # multiprocessing.pool.ApplyResult this form, the results need to be returned 
                # by the function value get removed
        results.append(s)
    sum_results = 0
    for res in results:
        sum_results += res.get()
                # Res.get value extracted here # () is of type int
 
    pool.close()
    pool.join()
    print(sum_results)

def demo_multiprocessing3():
    """This is to compare time with async/await
    So, you can see multiprocessing using 3 cores to compute, as a result,
    time for processing is less than async/await which only uses a single core
    """
    procs = 3

    # Create size segments list
    jobs = []
    for i in range(0, procs):
        jobs.append((i+1, 6))

    pool = Pool(procs).map(task, jobs)    

    print(pool)
    print(f"number of cpus: {multiprocessing.cpu_count()}")

if __name__ == "__main__":
    # n = int(1e8)
    # print(n)
    # start_time = time.time()
    # demo_multiprocessing1(n)
    # print(f"finished in {time.time() - start_time: .2f} seconds")

    # start_time = time.time()
    # demo_multiprocessing1(n)
    # print(f"finished in {time.time() - start_time: .2f} seconds")
    

    # print(f"In normal:")
    # start_time = time.time()
    # print(sum_nums([1, n]))
    # print(f"finished in {time.time() - start_time: .2f} seconds")

    start_time = time.time()
    demo_multiprocessing3()
    print(f"finished in {time.time() - start_time: .2f} seconds")

    
