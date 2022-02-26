import os
import argparse

from tqdm import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font_scale = 1.25)

def process_by_metric(sim_file, sim_num, metric):
    pre_sim_data = sim_file[sim_num + "_" + metric]

    if metric == "feature_metrics":
        sim_frame = pd.DataFrame(pre_sim_data)
        sim_data = sim_frame.rename(columns={0: "max", 1: "75", 2: "avg", 3: "25", 4: "min"})
    elif metric == "duplicate_classifiers":
        col_sums = list(np.sum(pre_sim_data, axis=0))
        while col_sums[-1] == 0:
            del col_sums[-1]
        sim_data = pd.DataFrame(pre_sim_data[:, 0:len(col_sums)])
    else:
        sim_data = pd.DataFrame(pre_sim_data)

    return sim_data

def smooth_sim_data(sim_data, n):
    return sim_data.rolling(n).sum() / n

def make_graph(sim_data, path):
    sim_plot = sns.relplot(data=sim_data, kind="line", dashes=False)
    # sns.move_legend(
    #     sim_plot, "upper center",
    #     bbox_to_anchor=(.5, 1), ncol=3, title=None, frameon=True,
    # )
    sim_plot.set(xlabel = "", ylabel = "")

    sim_plot.savefig(path) # bbox_inches = 'tight', pad_inches = 0

def main(args):
    in_dir = "./output/{}/data/".format(args.SIMSET)
    out_dir = "./output/{}/graphs/".format(args.SIMSET)
    os.makedirs(out_dir, exist_ok=True)

    metrics = ['feature_metrics', 'duplicate_classifiers']
    metric_short = {'feature_metrics': 'fm', 'duplicate_classifiers': 'dc'}

    for file in tqdm(os.listdir(in_dir)):
        if "sim" in file:
            path = os.path.join(in_dir, file)
            sim_file = np.load(path)
            sim_num = file.split(".")[0]
            for metric in metrics:
                sim_data = process_by_metric(sim_file, sim_num, metric)
                smooth_data = smooth_sim_data(sim_data, 10)

                graph_name = sim_num + "_" + metric_short[metric] + ".pdf"
                graph_path = os.path.join(out_dir, graph_name)
                make_graph(smooth_data, graph_path)

if __name__ == "__main__":
    print("Running visualization for summary data...")
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--SIMSET', type=str, required=True, help="Simulation set name")
    args = parser.parse_args()

    main(args)