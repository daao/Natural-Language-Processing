The project implements a constraint programming by using a library CP :
https://github.com/python-constraint/python-constraint

---- FILES
main.py : executable script
solver.py : class that create a problem, add constraints and variable and solve the problem
n_grams.py : read the file w2_.txt, construct the bi-gram matrix, normalize and compute the perplexity of a
sentence
constraints.json : contains semantic representations with the constraints, definition and the number of argument

--- USAGE
main.py --i <input_file>

The input file has a specific format as follow:
(string, var-1, value-1)
(string, var-2, value-2)
...

One constraint per line and each constraint is represented in "(...)" in which each component is separated by a comma.

--- Constraints
The list of constraint defined is in the file "constraints.json". You can add or modify the constraints in the file but
the maximum number of variables is 2. You can't create new constraints with more than 2 arguments. Some semantic
representation are provided. You can use those following semantics representations (not necessary all of them) but
more you define the constraints more precise the solution will be :
- (string, var-1, value-1) : define a variable and the value of variable.
- (first, var-1) : the variable needs to be the first word of the sentence.
- (last, var-1) : the variable needs to be the last word of the sentence.
- (meets, var-1, var-2) : The variable "var-1" needs to be before the variable "var-2" in the sentence.
- (precedes, var-1, var-2) : The variable "var-1" needs to PRECEDE DIRECTLY the variable "var-2" in the sentence.
- (follows, var-1 , var-2) : The variable "var-1" needs to be after the variable "var-2" in the sentence.