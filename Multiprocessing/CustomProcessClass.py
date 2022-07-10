from multiprocessing import Process, Value
from time import sleep



class CustomProcess(Process):
    def __init__(self):
        # Excute the base constructor
        Process.__init__(self)

        # Initialize integer value
        self.data = Value("i", 0)

    def run(self):
        # Block for a momment
        sleep(1)

        # Store the data variable
        self.data.value = 9

        # Print stored value
        print(f"Child stored: {self.data}")
        print(f"Child stored: {self.data.value}")

if __name__=="__main__":
    proc1 = CustomProcess()

    proc1.start()
    
    print("Waitting for the child process to finish")
    # Block until child process is terminated
    proc1.join()

    # Report the process attribute
    print(f"Parrent got: {proc1.data.value}")


