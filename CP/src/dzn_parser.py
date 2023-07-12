from os import listdir, makedirs
from os.path import isfile, join, exists
import numpy as np
import argparse


parser = argparse.ArgumentParser(description="Argument parser")
parser.add_argument(
    "--instances_dir", help="Path to instances folder", required=True, type=str
)
args = parser.parse_args()

onlyfiles = [
    f for f in listdir(args.instances_dir) if isfile(join(args.instances_dir, f))
]


basic_file_to_write = args.instances_dir + "/basic_model_dzn"
general_file_to_write = args.instances_dir + "/general_model_dzn"

print("Found files:")
print(onlyfiles)

if not exists(basic_file_to_write):
    makedirs(basic_file_to_write)

if not exists(general_file_to_write):
    makedirs(general_file_to_write)


def main():
    for f in onlyfiles:
        print("Working on {}".format(f))
        instance_file_read = open(args.instances_dir + "/" + f, "r")

        dzn_file_basic_model = open(
            basic_file_to_write + "/" + "basic_" + f.split(".")[0] + ".dzn", "w+"
        )

        dzn_file_general_model = open(
            general_file_to_write + "/" + "general_" + f.split(".")[0] + ".dzn", "w+"
        )

        # The first line contains the width and height of the enclosing rectangle
        first_line = instance_file_read.readline().strip().split(" ")

        # w = width
        dzn_file_basic_model.write("w = " + first_line[0] + ";\n")
        dzn_file_general_model.write("w = " + first_line[0] + ";\n")

        # h = height
        dzn_file_basic_model.write("h = " + first_line[1] + ";\n")
        dzn_file_general_model.write("h = " + first_line[1] + ";\n")

        # The second line contains the number of pieces to wrap
        second_line = instance_file_read.readline().strip().split(" ")

        # n = number of pieces;
        dzn_file_basic_model.write("n = " + second_line[0] + ";\n")
        dzn_file_general_model.write("n = " + second_line[0] + ";\n")

        # Extracting tiles dimensions from the rest of the file
        rest_of_lines = instance_file_read.readlines()

        # Removing possibly empty lines
        rest_of_lines = [line.strip() for line in rest_of_lines if line.strip()]

        # Extracting needed information:
        # - rectangles size: an array that contains only original rectangle in the basic_* files, and original + 90° rotated ones in general_* files;
        # - rectangles offset: always set to (0,0) and available only in general_* files;
        # - shape: an array of distinct shapes, accounting for rectangles and their rotations;
        # - shapeind: array that maps shapes to rectangles
        # - ncopy: count of distinct rectangles
        # - c: count of distinct tiles, useful in case of rectangles with the same shape

        dimensions = "dimension = ["
        rect_size = "rect_size = ["
        rect_offset = "rect_offset = ["
        shape = "shape = ["
        shapeind = "shapeind = ["
        i = 1
        ncopy = "ncopy = "
        pairs = {}

        for line in rest_of_lines:
            pair = line.replace(" ", "").strip()
            dimension = line.split(" ")
            if dimension[0] != dimension[1]:
                # Original rectangle
                rect_size += "|\n" + dimension[0] + ", " + dimension[1]
                rect_offset += "|\n" + str(0) + ", " + str(0)
                shape += "{" + str(i) + "}" + ", "
                shapeind += "{" + str(i) + ", "
                i += 1
                # Rotated rectangle
                rect_size += "|\n" + dimension[1] + ", " + dimension[0]
                rect_offset += "|\n" + str(0) + ", " + str(0)
                shape += "{" + str(i) + "}" + ", "
                shapeind += str(i) + "}, "
                i += 1
            else:
                rect_size += "|\n" + dimension[0] + ", " + dimension[1]
                rect_offset += "|\n" + str(0) + ", " + str(0)
                shape += "{" + str(i) + "}" + ", "
                shapeind += "{" + str(i) + "}, "
                i += 1
            dimensions += "|\n" + dimension[0] + ", " + dimension[1]
            pairs[pair] = pairs.get(pair, 0) + 1

        dimensions += "|];\n"

        i -= 1
        rect_size += "|];\n"
        rect_offset += "|];\n"
        shape = shape[:-2]
        shape += "];\n"
        shapeind = shapeind[:-2]
        shapeind += "];\n"

        ncopy += str(list(pairs.values())) + ";\n"

        # Writing files
        print("Writing files from {}".format(f))
        print()
        dzn_file_basic_model.write(dimensions)

        dzn_file_general_model.write("m = " + str(i) + ";\n")
        dzn_file_general_model.write(rect_size)
        dzn_file_general_model.write(rect_offset)
        dzn_file_general_model.write(shape)
        dzn_file_general_model.write(shapeind)
        dzn_file_general_model.write(ncopy)
        dzn_file_general_model.write(
            "c = " + str(np.array([list(pairs.values())]).size) + ";\n"
        )

        # Closing files
        print("Closing files...")
        print()
        instance_file_read.close()
        dzn_file_basic_model.close()
        dzn_file_general_model.close()


if __name__ == "__main__":
    main()