import ctypes
import time

STD_OUTPUT_HANDLE= -11
hOut = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
empty_line = "\t\t\t\t\t\t\t\t"

class COORD(ctypes.Structure):
	 _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)] 
	 def __init__(self,x,y):
		 self.X = x
		 self.Y = y

def goto_xy(x=0, y=0):
    INIT_POS=COORD(y,x)
    ctypes.windll.kernel32.SetConsoleCursorPosition(hOut,INIT_POS)

if __name__ == "__main__":
    for i in range(20):
        goto_xy(5, 0)
        print(empty_line)
        goto_xy(5, 0)
        print(f"{i}%")
        time.sleep(1)
        