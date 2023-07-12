include "globals.mzn";

%%%% Data and variables declaration section %%%%

int: n; % Number of rectangles
int: w; % Paper width
int: h; % Paper heigth

set of int: TILES= 1..n;
array[TILES, 1..2] of int: dimension; % Dimensions of tiles

% Variables
array[TILES, 1..2] of var int: coords; % Bottom left corner coordinates

%%%% Constraints section %%%%

% Bottom left corner constraint
constraint forall(i in TILES)
                 ((coords[i,1] >= 0 /\ coords[i,1] <= w - dimension[i,1]) 
               /\ (coords[i,2] >= 0 /\ coords[i,2] <= h - dimension[i,2]));


% Non-overlap constraint (Reference: 4.2.6.6 Packing constraint from minizinc tutorial) 
constraint diffn(coords[..,1],coords[..,2], dimension[..,1], dimension[..,2]);                
                        
% Constraint on the paper size (= paper capacity) --> This is a redundant constraint: needed to improve constraint propagation
constraint cumulative(coords[..,1], dimension[..,1], dimension[..,2], h); % Vertical constraint
constraint cumulative(coords[..,2], dimension[..,2], dimension[..,1], w); % Horizontal constraint

% Symmetry breaking constraint: set the most difficult to place rectangle, i.e. the biggest one, in the position (0,0)
constraint coords[arg_max([dimension[i,1]*dimension[i,2] | i in TILES]),1] = 0;
constraint coords[arg_max([dimension[i,1]*dimension[i,2] | i in TILES]),2] = 0;

%%%% Search section %%%%

% Trying different search strategies
ann:search_ann;
% search_ann = int_search(coords, first_fail, indomain_min, complete);
% search_ann = int_search(coords, first_fail, indomain_max, complete);
% search_ann = int_search(coords, first_fail, indomain_median, complete);
% search_ann = int_search(coords, first_fail, indomain_split, complete);
% search_ann = int_search(coords, first_fail, indomain_reverse_split, complete);
% search_ann = int_search(coords, first_fail, indomain_random, complete);


% search_ann = int_search(coords, dom_w_deg, indomain_min, complete);
% search_ann = int_search(coords, dom_w_deg, indomain_max, complete);
% search_ann = int_search(coords, dom_w_deg, indomain_median, complete);
search_ann = int_search(coords, dom_w_deg, indomain_split, complete);
% search_ann = int_search(coords, dom_w_deg, indomain_reverse_split, complete);
% search_ann = int_search(coords, dom_w_deg, indomain_random, complete);


% search_ann = int_search(coords, anti_first_fail, indomain_min, complete);
% search_ann = int_search(coords, anti_first_fail, indomain_max, complete);
% search_ann = int_search(coords, anti_first_fail, indomain_median, complete);
% search_ann = int_search(coords, anti_first_fail, indomain_split, complete);
% search_ann = int_search(coords, anti_first_fail, indomain_reverse_split, complete);
% search_ann = int_search(coords, anti_first_fail, indomain_random, complete);


% search_ann = int_search(coords, smallest, indomain_min, complete);
% search_ann = int_search(coords, smallest, indomain_max, complete);
% search_ann = int_search(coords, smallest, indomain_median, complete);
% search_ann = int_search(coords, smallest, indomain_split, complete);
% search_ann = int_search(coords, smallest, indomain_reverse_split, complete);
% search_ann = int_search(coords, smallest, indomain_random, complete);

% search_ann = int_search(coords, input_order, indomain_min, complete);
% search_ann = int_search(coords, input_order, indomain_max, complete);
% search_ann = int_search(coords, input_order, indomain_median, complete);
% search_ann = int_search(coords, input_order, indomain_split, complete);
% search_ann = int_search(coords, input_order, indomain_reverse_split, complete);
% search_ann = int_search(coords, input_order, indomain_random, complete);

% search_ann = int_search(coords, largest, indomain_min, complete);
% search_ann = int_search(coords, largest, indomain_max, complete);
% search_ann = int_search(coords, largest, indomain_median, complete);
% search_ann = int_search(coords, largest, indomain_split, complete);
% search_ann = int_search(coords, largest, indomain_reverse_split, complete);
% search_ann = int_search(coords, largest, indomain_random, complete);



solve :: search_ann 
%        :: restart_luby(1000)
       satisfy;
      
% Print solutions
output [show(w) ++ " " ++ show(h) ++ "\n"];
output [show(n) ++ "\n"];
% output [show(arg_max([dimension[i,1]*dimension[i,2] | i in TILES])) ++ "\n"];


output [
  show(dimension[i,1]) ++ " " ++ show(dimension[i,2]) ++ "   " ++ show(coords[i,1]) ++ " " ++ show(coords[i,2]) ++ "\n"
  | i in TILES
];
