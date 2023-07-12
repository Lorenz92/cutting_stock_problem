from os import listdir, makedirs
from os.path import isfile, join, exists
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.patches import Rectangle
from matplotlib.ticker import MultipleLocator
import argparse


parser = argparse.ArgumentParser(description="Argument parser")
parser.add_argument(
    "--dir_to_plot", help="Path to folder of files to plot", required=True, type=str
)
args = parser.parse_args()

dir_to_write = args.dir_to_plot + "/graph/"


if not exists(dir_to_write):
    makedirs(dir_to_write)

onlyfiles = [
    f
    for f in listdir(args.dir_to_plot)
    if isfile(join(args.dir_to_plot, f)) and (f.split(".")[1] == "txt")
]

print("Found files:")
print(onlyfiles)
print()

for f in onlyfiles:
    file_reading = open(args.dir_to_plot + "/" + f, "r")
    print("working on {}".format(f))

    # Extracting width and height
    first_line = file_reading.readline().strip().split(" ")

    w = int(first_line[0])
    h = int(first_line[1])

    # Extracting the number of tiles to draw
    second_line = file_reading.readline().strip().split(" ")

    number_of_tiles = int(second_line[0])

    # Extracting dimensions and positions of rectangles
    rest_of_lines = file_reading.readlines()

    # Removing possibly empty lines
    rest_of_lines = [line.strip() for line in rest_of_lines if line.strip()]

    tiles = []

    for i, line in enumerate(rest_of_lines):

        line = line.split()
        tiles.append([int(i) for i in line])

    fig = plt.figure(figsize=(5 + (w // 10), 5 + (h // 10)))
    ax = fig.gca(title="Solution plot for the {} case".format(f.split("-")[0]))
    for i in range(number_of_tiles):
        color = ["#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])]
        rect = Rectangle(
            (tiles[i][2], tiles[i][3]),
            tiles[i][0],
            tiles[i][1],
            fill=True,
            color=color[0],
            alpha=0.3,
        )
        ax.add_patch(rect)
    plt.plot()
    # plt.show()

    print("Saving graph for {} case".format(f.split(".")[0]))
    print()
    plt.savefig(dir_to_write + f.split(".")[0] + ".png")
    plt.close()

    file_reading.close()

print()
print("Execution completed.")
