import sys
import numpy as np
import random

MAX_VAL = 100000

if len(sys.argv) != 5:
    print("Usage : %s <output_path> <num_row> <num_col> <dup_percent>" % (sys.argv[0]))
    exit(-1)

out_path = sys.argv[1]
num_row = int(sys.argv[2])
num_col = int(sys.argv[3])
dup_percent = int(sys.argv[4])

tot = 0

with open(out_path, "w") as f:

    while True:
        rows = np.random.randint(low=0, high=MAX_VAL, size=(100, num_col))

        st = "\n".join([" ".join(r.astype(np.str).tolist()) for r in rows]) + "\n"
        f.write(st)
        tot += rows.shape[0]

        dp_idx = np.random.choice(100, dup_percent, replace=False)
        dp_rows = rows[dp_idx]

        st = "\n".join([" ".join(r.astype(np.str).tolist()) for r in dp_rows]) + "\n"
        f.write(st)
        tot += dp_rows.shape[0]

        if tot > num_row:
            break
