import os
import numpy as np

def main():
    dir = "./output/data/sims"
    output = {}

    for file_name in os.listdir(dir):
        f = os.path.join(dir, file_name)
        np_f = np.load(f)
        for entry in np_f.files:
            output[entry] = np_f[entry]

    np.savez(os.path.join(dir, "merged.npz"), **output)

if __name__ == "__main__":
    main()