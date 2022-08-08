import os
import numpy as np
import mmap

current_dir_path = os.path.dirname(os.path.realpath(__file__))

class CSVShuffler:
    def __init__(self, input_file:str = None, header=True, batch_size=1000):
        self.input_file=input_file
        self.header=header
        self.batch_size=batch_size

    def shuffle_csv(self):
        """Read input file and shuffle
        """
        with open(file=self.input_file, mode="r", encoding="utf-8-sig") as fi:
            with mmap.mmap(fi.fileno(), length=0, access=mmap.ACCESS_READ) as file_map:
                lines = file_map.read().decode("utf-8-sig").splitlines()

                if self.header:
                    header=lines[0]

                lines = lines[1:]

                if self.batch_size <= len(lines):
                    self.batch_size = len(lines)

                np.random.shuffle(lines)
            

        """Write score to output file
        """
        with open(f"{current_dir_path}\\output.txt", "w") as fo:
            # Write header
            fo.write(header+"\n")

            for batch in range(0, len(lines), self.batch_size):
                fo.write('\n'.join([line for line in lines[batch: batch + self.batch_size]]))

        
        return len(lines)
