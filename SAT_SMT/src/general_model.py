from os import listdir, makedirs
from os.path import isfile, join, exists
import argparse
import numpy as np
from z3 import *
import matplotlib.pyplot as plt
import random
from matplotlib.patches import Rectangle


out_dir = "../out/general_model_smt"
graph_dir = out_dir + '/graph/'
stats_dir = out_dir + "/stats/"

parser = argparse.ArgumentParser(description='Argument parser')
parser.add_argument("--instances_dir", help="Path to instances folder", required = True, type=str)
parser.add_argument("--file_name", help="Instance file to solve", required = False, type=str)
args = parser.parse_args()

if not exists(out_dir):
    makedirs(out_dir)

if not exists(graph_dir):
    makedirs(graph_dir)

if not exists(stats_dir):
    makedirs(stats_dir)

def main():
    files = []
     
    print(args.instances_dir)

    if(args.file_name):
        print(args.file_name)
        files.append(args.file_name)
    else:
        files = [f for f in listdir(args.instances_dir) if isfile(join(args.instances_dir, f))] 
    
    print(files)
    for file in files:
    
        print("Working on {}".format(file))

        instance_file_read = open(args.instances_dir + "/" + file, "r")

        output_file_basic_model = open(
            out_dir + "/" + "general_" + file.split(".")[0] + "-out.txt", "w+"
        )

        statistic_file = open(
            stats_dir + "general_" + file.split(".")[0] + "-statistics.txt", "w+"
        )

        ###################     Data     ###################
        print("Declaring problem data...")

        # The first line contains the width and height of the enclosing rectangle
        first_line = instance_file_read.readline().strip().split(" ")

        # w = width
        w = int(first_line[0])

        # h = height
        h = int(first_line[1])

        # The second line contains the number of pieces to wrap
        second_line = instance_file_read.readline().strip().split(" ")

        # n = number of pieces;
        n = int(second_line[0])
        TILES = range(int(str(n)))

        # Extracting the tiles dimensions from the rest of the file
        rest_of_lines = instance_file_read.readlines()

        # Removing possibly empty lines
        rest_of_lines = [line.strip() for line in rest_of_lines if line.strip()]

        # Building a shape tensor where each element is the couple of the two different orientations for each rectangle
        # Squares of sides "dim" are modeled as the couple [[dim, dim],[-99, -99]] to allow only one configuration and respect the tensor shape.
        # Obviously they could be treated as the tensor [[dim, dim],[dim, dim]] but this would generate symmetric configuration.

        shape = []
        count_of_shapes = {}

        for line in rest_of_lines:
            dims = []

            rectangle = [int(line.split(" ")[0]), int(line.split(" ")[1])]
            dims.append(rectangle)

            key = "{}x{}".format(rectangle[0], rectangle[1])
            count_of_shapes[key] = count_of_shapes.get(key, 0) + 1

            if rectangle[0] != rectangle[1]:
                dims.append([rectangle[1], rectangle[0]])
                shape.append(dims) #TODO: portare fuori dall'if
            else:
                dims.append([-99, -99])
                shape.append(dims)

        ncopy = list(count_of_shapes.values())
        num_distinct_tiles = np.array([ncopy]).size

        ###################     Variables     ###################
        print("Declaring variables...")

        # 1. coords_i_j is the jth coordinate of bottom left corner of ith rectangle
        coords = [[Int("coords_%s_%s" % (i + 1, j + 1)) for j in range(2)] for i in TILES]

        # 2. dimension_i_j is the length of jth side of ith rectangle.
        # The purpose of this variable is to handle the rectangle rotations.
        dimension = [
            [Int("dimension_%s_%s" % (i + 1, j + 1)) for j in range(2)] for i in TILES
        ]

        ###################     Constraints     ###################
        print("Building up constraints...")

        # Bottom left corner constraint
        bl_constraint = [
            And(
                coords[i][0] >= 0,
                coords[i][0] <= w - dimension[i][0],
                coords[i][1] >= 0,
                coords[i][1] <= h - dimension[i][1],
            )
            for i in TILES
        ]

        # No-overlap constraint
        no_overlap_constraint = [
            Or(
                coords[i][0] + dimension[i][0] <= coords[j][0],
                coords[j][0] + dimension[j][0] <= coords[i][0],
                coords[i][1] + dimension[i][1] <= coords[j][1],
                coords[j][1] + dimension[j][1] <= coords[i][1],
            )
            for i in TILES
            for j in TILES
            if j > i
        ]

        # Implied constraint - "cumulative" in MiniZinc
        cumulative_constraint = []

        # 1.Cumulative on heigth capacity:
        for i in range(w):
            vertical_sum = Sum(
                [
                    If(
                        And(coords[j][0] <= i, coords[j][0] + dimension[j][0] > i),
                        dimension[j][1],
                        0,
                    )
                    for j in TILES
                ]
            )
            cumulative_constraint.append(vertical_sum <= h)

        # 2.Cumulative on width capacity:
        for i in range(h):
            horizontal_sum = Sum(
                [
                    If(
                        And(coords[j][1] <= i, coords[j][1] + dimension[j][1] > i),
                        dimension[j][0],
                        0,
                    )
                    for j in TILES
                ]
            )
            cumulative_constraint.append(horizontal_sum <= w)

        # Symmetry breaking constraints

        # 1. isomorphisms breaking
        surface = [
            shape[i][j][0] * shape[i][j][1]
            for i in range(num_distinct_tiles)
            for j in range(1)
        ]
        biggest_rect = np.argmax(np.array(surface))

        symm_break = [And(coords[biggest_rect][0] == 0, coords[biggest_rect][1] == 0)]

        # 2. Ordering symmetries breaking for rectangles with the same size - this constraint comes into play only when there are rectangles with the same size
        order_constraint = []
        base = []

        for i in range(num_distinct_tiles):
            if i == 0:
                base.append(0)
            else:
                base.append(sum(ncopy[0:i]))

        for i in range(num_distinct_tiles):
            for j in range(ncopy[i] - 1):
                order_constraint.append(
                    And(
                        coords[base[i] + j][0] <= coords[base[i] + j + 1][0],
                        Implies(
                            coords[base[i] + j][0] == coords[base[i] + j + 1][0],
                            coords[base[i] + j][1] <= coords[base[i] + j + 1][1],
                        ),
                    )
                )


        # Allow the algorithm to select only one rotation among the two possible ones of a rectangle
        rotation_constraint = [
            Or(
                And(shape[i][0][0] == dimension[i][0], shape[i][0][1] == dimension[i][1]),
                And(
                    shape[i][1][0] == dimension[i][0],
                    shape[i][1][1] == dimension[i][1],
                    dimension[i][0] != -99,
                    dimension[i][1] != -99,
                ),
            )
            for i in TILES
        ]
        # ------------------------------------------------------------------

        constraints = (
              bl_constraint
            + no_overlap_constraint
            # + cumulative_constraint
            # + order_constraint
            # + symm_break
            + rotation_constraint
        )

        ###################     Solving     ###################
        print("Solving...")

        s = Solver()
        s.add(constraints)

        fig = plt.figure(figsize=(5 + (int(str(w)) // 8), 5 + (int(str(h)) // 8)))
        ax = fig.gca(title="Plot of the solution")

        if s.check() == sat:
            m = s.model()

            print("{} {}".format(h, w))
            output_file_basic_model.write("{} {}\n".format(h, w))

            print("{}".format(n))
            output_file_basic_model.write("{}\n".format(n))

            for i in TILES:
                print(
                    "{:<1} {:<3} {:<1} {:<2}".format(
                        str(m[dimension[i][0]]),
                        str(m[dimension[i][1]]),
                        str(m[coords[i][0]]),
                        str(m[coords[i][1]]),
                    )
                )
                output_file_basic_model.write(
                    "{:<1} {:<3} {:<1} {:<2}\n".format(
                        str(m[dimension[i][0]]),
                        str(m[dimension[i][1]]),
                        str(m[coords[i][0]]),
                        str(m[coords[i][1]]),
                    )
                )
                color = [
                    "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
                ]
                rect = Rectangle(
                    (m[coords[i][0]].as_long(), m[coords[i][1]].as_long()),
                    m[dimension[i][0]].as_long(),
                    m[dimension[i][1]].as_long(),
                    fill=True,
                    color=color[0],
                    alpha=0.3,
                )

                ax.add_patch(rect)

            print("\n{}\n".format(s.statistics()))
            statistic_file.write(str(s.statistics()))

            plt.plot()
            # plt.show()
            print("Saving graph for {} case".format(file.split(".")[0]))
            plt.savefig(graph_dir + file.split(".")[0] + ".png")
            plt.close('all')
        else:
            print("<<< UNSAT >>>")


if __name__ == "__main__":
    main()
