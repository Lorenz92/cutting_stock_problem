from os import listdir, makedirs
from os.path import isfile, join, exists
import argparse
import numpy as np
import pandas as pd

out_dir = "./"

parser = argparse.ArgumentParser(description='Argument parser')
parser.add_argument("--stats_dir", help="Path to instances folder", required = True, type=str)

args = parser.parse_args()

def main():
    files = []
     
    print(args.stats_dir)

    files = [f for f in listdir(args.stats_dir) if isfile(join(args.stats_dir, f))]

    instance = []
    conflicts = []
    time = []

    model = args.stats_dir.split('/')[-2]

    print(files)
    for file in files:
       
        print("Working on {}".format(file))
        
        instance_file_read = open(args.stats_dir + '/' + file, "r")

        # Extracting lines
        lines = instance_file_read.readlines()

        # Removing possibly empty lines ---> TODO:controllare se possibile eliminare
        rest_of_lines = [line.strip() for line in lines if line.strip()]

        filename = file.split('-')[0].split('_')[1:]
        print(filename)

        if len(filename) > 1:
            filename = '_'.join(filename)
        else:
            filename = filename[0]

        instance.append(filename)

        for line in rest_of_lines:
            
            if line.split(" ")[0] == ':conflicts':
                conflicts.append(line.split(" ")[-1].strip())
                
            if line.split(" ")[0] == ':time':
                time.append(line.split(" ")[-1].strip().replace(')',''))
        
        instance_file_read.close()

    data = {'instance': instance, 'conflicts':conflicts, 'time': time}
    df = pd.DataFrame(data)

    print('Saving csv in current directory...')
    df.to_csv(model + '_stats_compare.csv', index=False)
    print('Saved.')


if __name__ == "__main__":
    main()
