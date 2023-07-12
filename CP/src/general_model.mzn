include "globals.mzn";

%%%% Data and variables declaration section %%%%

int: n; % Number of tiles/rectangles
int: w; % Paper width
int: h; % Paper heigth
int: m; % Number of possible shapes: original rectangles + their rotations

set of int: DRECT = 1..m;
set of int: ROT=1..2; % Different positioning of the same rectangles: original position and 90° rotated position.
set of int: TILES = 1..n;

% Following data are needed for geost_bb constraint
array[int] of set of DRECT: shape; % List of distinct shape that takes into account rotated rectangles
array[TILES] of set of int: shapeind; % Indices of original and rotated rectangles
array[DRECT, 1..2] of int: rect_size; % Rectangles dimensions
array[DRECT, 1..2] of int: rect_offset; % Rectangles offsets -> in this problem always 0

int: c;
set of int: NUMDISTINCTTILES = 1..c;
array[NUMDISTINCTTILES] of int: ncopy; % Number of copies for each rectangle

% Variables
array[TILES, 1..2] of var int: coords; % Bottom left corner coordinates
array[TILES] of var int: kind; % The selected rotation among the two allowed


%%%% Constraints section %%%%
       
% Bottom left corner constraint
constraint forall(i in TILES)
                 ((coords[i,1] >= 0 /\ coords[i,1] <= w - rect_size[kind[i],1]) /\ (coords[i,2] >= 0 /\ coords[i,2] <= h - rect_size[kind[i],2]));
                 
% Non-overlap constraint
constraint forall(i in TILES)(kind[i] in shapeind[i]);
constraint geost_bb(2,
                      rect_size,
                      rect_offset,
                      shape,
                      coords,
                      kind,
                      [0,0],
                      [w,h]);

% Constraint on the paper size
constraint cumulative([coords[i,1] | i in TILES], [rect_size[kind[i],1] | i in TILES], [rect_size[kind[i],2] | i in TILES], h); % Vertical constraint
constraint cumulative([coords[i,2] | i in TILES], [rect_size[kind[i],2] | i in TILES], [rect_size[kind[i],1] | i in TILES], w); % Horizontal constraint
    

% Symmetry breaking: set the most difficult to place rectangle, i.e. the biggest one, in the position (0,0)
% constraint coords[arg_max([rect_size[kind[i],1]*rect_size[kind[i],2] | i in TILES]),1] = 0;
% constraint coords[arg_max([rect_size[kind[i],1]*rect_size[kind[i],2] | i in TILES]),2] = 0;


% Ordering constraint: needed to break ordering symmetries

% Generating an array of indeces for the distinct sizes in dimension
% e.g. for the istance = 16x16_symmetry -> base=[0,4,5,6,7,8,9] of length NUMDISTINCTTILES
array[NUMDISTINCTTILES] of int: base = [if i = 1 then 0 else sum(j in 1..i-1)(ncopy[j]) endif | i in NUMDISTINCTTILES];

% Ordering pieces: this comes into play only for rectangles with the same size
constraint forall(i in NUMDISTINCTTILES)(
  forall(j in 1..ncopy[i]-1)(
%     lex_less(coords[base[i]+j,..],coords[base[i]+j+1,..])));
      lex_greater(coords[base[i]+j,..],coords[base[i]+j+1,..])));


%%%% Search section %%%%

% Trying different search strategies
ann:search_ann;
% search_ann = int_search(kind, first_fail, indomain_min, complete);
% search_ann = int_search(kind, first_fail, indomain_max, complete);
% search_ann = int_search(kind, first_fail, indomain_median, complete);
% search_ann = int_search(kind, first_fail, indomain_split, complete);
% search_ann = int_search(kind, first_fail, indomain_reverse_split, complete);
% search_ann = int_search(kind, first_fail, indomain_random, complete);


% search_ann = int_search(kind, dom_w_deg, indomain_min, complete);
% search_ann = int_search(kind, dom_w_deg, indomain_max, complete);
% search_ann = int_search(kind, dom_w_deg, indomain_median, complete);
search_ann = int_search(kind, dom_w_deg, indomain_split, complete);
% search_ann = int_search(kind, dom_w_deg, indomain_reverse_split, complete);
% search_ann = int_search(kind, dom_w_deg, indomain_random, complete);


% search_ann = int_search(kind, anti_first_fail, indomain_min, complete);
% search_ann = int_search(kind, anti_first_fail, indomain_max, complete);
% search_ann = int_search(kind, anti_first_fail, indomain_median, complete);
% search_ann = int_search(kind, anti_first_fail, indomain_split, complete);
% search_ann = int_search(kind, anti_first_fail, indomain_reverse_split, complete);
% search_ann = int_search(kind, anti_first_fail, indomain_random, complete);


% search_ann = int_search(kind, smallest, indomain_min, complete);
% search_ann = int_search(kind, smallest, indomain_max, complete);
% search_ann = int_search(kind, smallest, indomain_median, complete);
% search_ann = int_search(kind, smallest, indomain_split, complete);
% search_ann = int_search(kind, smallest, indomain_reverse_split, complete);
% search_ann = int_search(kind, smallest, indomain_random, complete);

% search_ann = int_search(kind, input_order, indomain_min, complete);
% search_ann = int_search(kind, input_order, indomain_max, complete);
% search_ann = int_search(kind, input_order, indomain_median, complete);
% search_ann = int_search(kind, input_order, indomain_split, complete);
% search_ann = int_search(kind, input_order, indomain_reverse_split, complete);
% search_ann = int_search(kind, input_order, indomain_random, complete);

% search_ann = int_search(kind, largest, indomain_min, complete);
% search_ann = int_search(kind, largest, indomain_max, complete);
% search_ann = int_search(kind, largest, indomain_median, complete);
% search_ann = int_search(kind, largest, indomain_split, complete);
% search_ann = int_search(kind, largest, indomain_reverse_split, complete);
% search_ann = int_search(kind, largest, indomain_random, complete);



solve :: search_ann 
%        :: restart_luby(1000)
       satisfy;


% Print solutions
output [show(w) ++ " " ++ show(h) ++ "\n"];
output [show(n) ++ "\n"];
% output [show(arg_max([rect_size[kind[i],1]*rect_size[kind[i],2] | i in TILES])) ++ "\n"];

output [
  show(rect_size[kind[i],1]) ++ " " ++ show(rect_size[kind[i],2]) ++ "   " ++ show(coords[i,1]) ++ " " ++ show(coords[i,2]) ++ "\n"
  | i in TILES
];


