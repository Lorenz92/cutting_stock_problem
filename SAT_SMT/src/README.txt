//////////////////////////////////////////////////////
//       basic_model.py - general_model.py          //
//////////////////////////////////////////////////////

Both the scripts accept two input parameters:

- instances_dir: absolute path to instances folder. It is mandatory.
- file_name: name of the single .txt file to solve (e.g. "8x8.txt"). The file has to be present in the instance_dir provided. It is NOT mandatory.

Both the scripts generate the folder "out" in the parent directory of the program current directory (where the program runs).
This folder will contain instances solutions.
Then, they create the folders "out/graph" and "out/stats" that contain graphical representation of solutions and solving statistics provided by Z3 default output.


////////////////////////////////
//       stas_parser.py       //
////////////////////////////////

This is an auxiliary script used to build tables of results.
It accept only one mandatory input parameter "stats_dir" that is the path to "out/stats" and save a .csv containing a table with the columns: "instance", "conflicts" and "time", in the current directory.

