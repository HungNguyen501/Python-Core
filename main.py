from cmath import sqrt
import numpy as np
import pandas as pd
from math import sqrt


import random

# open file object by replacing filename with name of the file
file_object = open("D:\\Projects\\Python\\input.txt")

# initialize random_txt and line_number with '' and 0 respectively
random_txt = ''
line_number = 0

while True:
    
    # read a line in one iteration
    line = file_object.readline()
    
    # if no more lines, break
    if not line:
        break
    
    line_number += 1
    prob = random.uniform(0, line_number)
    
    if prob <= 1:
        random_txt = line 
        print(f"{line_number}: {random_txt}   {prob}")
        print(1/line_number)

# print(random_txt)