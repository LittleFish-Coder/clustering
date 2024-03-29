import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import argparse
import time
import matplotlib.pyplot as plt


def load_data(input_file):
    data = np.loadtxt(input_file, delimiter=" ")
    print(data.shape)  # (1092, 2)
    return data


def normalize(data):
    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    return data


def plot_data(data, eps, min_samples, labels, input_file):

    plt.figure(figsize=(11, 6))
    plt.suptitle(f"DBSCAN Clustering with eps: {eps} and min_samples: {min_samples}\n{input_file}")

    plt.subplot(1, 2, 1)
    plt.title("Original Data")
    plt.scatter(data[:, 0], data[:, 1])

    plt.subplot(1, 2, 2)
    plt.title("Clustered Data")
    plt.scatter(data[:, 0], data[:, 1], c=labels)
    plt.savefig(input_file + "_output.png")
    plt.show()


def dbscan_clustering(data, eps=0.1, min_samples=20):
    # hyperparameters
    # eps: The maximum distance between two samples for one to be considered as in the neighborhood of the other.
    # min_samples: The number of samples (or total weight) in a neighborhood for a point to be considered as a core point.
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(data)
    labels = db.fit_predict(data)
    return labels


def output_data(data, eps, min_samples, labels, output_path):
    with open(output_path, "w") as f:
        f.write(f"DBSCAN -- eps: {eps}, min_samples: {min_samples}\n")
        f.write("X Y ClusterID\n")
        for i in range(data.shape[0]):
            f.write(f"{data[i, 0]} {data[i, 1]} {labels[i]}\n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Apriori Algorithm")
    parser.add_argument(
        "--input", type=str, default="Clustering_testdata/Clustering_test1", help="input file name"
    )
    parser.add_argument("--eps", type=float, default=0.265, help="eps")
    parser.add_argument("--min_samples", type=int, default=20, help="min_samples")
    parser.add_argument("--output", type=str, default="output", help="output file name")
    args = parser.parse_args()

    input_file = args.input
    eps = args.eps
    min_samples = args.min_samples
    output_path = input_file + "_output.txt"
    print(f"input file: {input_file}")
    print(f"eps: {eps}")
    print(f"min_samples: {min_samples}")
    print(f"output path: {output_path}")

    ##### start time #####
    start = time.time()
    data = load_data(input_file)
    data = normalize(data)
    labels = dbscan_clustering(data, eps=eps, min_samples=min_samples)
    end = time.time()
    ##### end time #####
    print(f"Time: {end - start} seconds")

    # Extract the unique cluster labels
    unique_clusters = set(labels)
    print(labels)
    print(unique_clusters)
    plot_data(data, eps, min_samples, labels, input_file)

    # Write the output to a file
    output_data(data, eps, min_samples, labels, output_path)


# Output Format:
# X, Y, ClusterID
# 0.1, 0.1, 0
