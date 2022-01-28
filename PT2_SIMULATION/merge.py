import os
import argparse

import numpy as np
from tqdm import tqdm

def main(args):
    dir = "./output/summary/data"
    output = {}

    for file_name in tqdm(os.listdir(dir)):
        f = os.path.join(dir, file_name)
        np_f = np.load(f)
        for entry in np_f.files:
            output[entry] = np_f[entry]

    np.savez(os.path.join(dir, "merged.npz"), **output)

if __name__ == "__main__":
    print("Running merge...")

    parser = argparse.ArgumentParser()
    parser.add_argument('--SIMSET', type=str, required=True, help="Simulation set name")
    args = parser.parse_args()

    main(args)