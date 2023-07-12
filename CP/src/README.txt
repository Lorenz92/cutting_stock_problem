//////////////////////////////////
//       dzn_parser.py          //
//////////////////////////////////

How to run: dzn_parser.py --instances_dir=<instance_dir>, 
where instance_dir is the path to instance folder.

This script will automatically generate two folders "<instance_dir>/basic_model_dzn" and "<instance_dir>/general_model_dzn"
that will contain the ready-to-be-used dzn files for the Minizinc programs.


//////////////////////////////////
//    results_to_graph.py       //
//////////////////////////////////

How to run: results_to_graph.py --dir_to_plot=<dir_to_plot>, where dir_to_plot is the path to the folder that contains
the solutions of Minizinc programs in .txt format.

This script will automatically generate the folder <dir_to_plot>/graph that will contains the plot of Minizinc results.