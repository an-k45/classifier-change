import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

def unpack_single_npz(path):
    sim_file = np.load(path)
    sim_data = pd.DataFrame(sim_file[sim_file.files[0]])
    return sim_data.rename(columns={0: "min", 1: "max", 2: "avg"})

def smooth_sim_data(sim_data, n):
    return sim_data.rolling(n).sum() / n

def make_graph(sim_data, path):
    sim_plot = sns.relplot(data=sim_data, kind="line")
    sim_plot.savefig(path)

def main():
    in_dir = "./output/summary/data"
    out_dir = "./output/summary/graphs"

    for file in os.listdir(in_dir):
        if "sim" in file:
            path = os.path.join(in_dir, file)
            graph_path = os.path.join(out_dir, file.split(".")[0] + ".png")

            sim_data = unpack_single_npz(path)
            smooth_data = smooth_sim_data(sim_data, 10)
            make_graph(smooth_data, graph_path)

if __name__ == "__main__":
    main()