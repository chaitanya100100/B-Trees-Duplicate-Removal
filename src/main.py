import sys
import os
from MyHash import MyHash
from BTree import BTree

BLOCK_SIZE = 512 # in bytes

class DuplicateElimination(object):

    def __init__(self, input_file, output_file, MMB, index_type):

        self.input_file = input_file
        self.output_file = output_file
        self.MMB = MMB

        if index_type == "btree":
            self.index = BTree()
        elif index_type == "hash":
            self.index = MyHash()
        else:
            print("Invalid index type")
            exit(-1)

        self.dup_open()

        while True:
            rec = self.get_next()

            # input file finished
            if rec == None:
                self.flush_output()
                break

            # append the record to output buffer if unique
            if not self.index.search(rec):
                self.out_buff.append(rec)
                self.index.insert(rec)

            # if output buffer is full then flush the output
            if len(self.out_buff) >= self.NTB:
                self.flush_output()

        self.dup_close()


    def flush_output(self):
        if len(self.out_buff) == 0:
            return

        # write to output file
        #----------------------
        st = "\n".join([" ".join(list(map(str, r))) for r in self.out_buff]) + "\n"
        self.out_fd.write(st)

        del self.out_buff[:]


    def dup_open(self):
        with open(self.input_file, "r") as f:
            self.NR = sum(1 for line in f if line.rstrip())

        with open(self.input_file, "r") as f:
            for line in f:
                if line.rstrip():
                    self.NC = len(line.rstrip().split())
                    break

        # assuming that each value in tuple is 32-bit (4-byte) int
        self.NTB = int(BLOCK_SIZE / (4 * self.NC))

        print("MMB = number of main memory blocks = ", self.MMB)
        print("NTB = number of tuples in a block = ", self.NTB)

        self.out_buff = []
        self.inp_buff = [[] for i in range(self.MMB - 1)]

        self.inp_idx = 0

        self.inp_fd = open(self.input_file, "r")
        self.out_fd = open(self.output_file, "w")


    def dup_close(self):
        self.inp_fd.close()
        self.out_fd.close()


    def get_next(self):

        for ib in self.inp_buff:
            if len(ib) == 0:
                for i in range(self.NTB):
                    row = self.inp_fd.readline()
                    if not row: break
                    row = [int(c) for c in row.rstrip().split()]
                    ib.append(row)

            if len(ib) != 0:
                return ib.pop(-1)

        return None


if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Usage : %s <input_file> <output_file> <index_type> <num_blocks>")
        exit(-1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    index_type = sys.argv[3]
    MMB = int(sys.argv[4])

    if not os.path.isfile(input_file):
        print("Invalid input file")
        exit(-1)

    if index_type not in ["btree", "hash"]:
        print("Invalid index type")
        exit(-1)

    DuplicateElimination(input_file, output_file, MMB, index_type)
