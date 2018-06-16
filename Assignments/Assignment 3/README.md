The project implements a constraint programming by using a library CP :
https://github.com/python-constraint/python-constraint

## FILES
main.py : executable script
solver.py : class that create a problem, add constraints and variables and solve the problem
n_grams.py : read the file w2_.txt, construct the bi-gram matrix, normalize and compute the perplexity of a
sentence
constraints.json : contains semantic representations with the constraints, a comment, an array of indices and the number of arguments

## USAGE
<pre> <code>
main.py -i input_file
</code></pre>

The input file has a specific format as follow:
(string, var-1, value-1)
(string, var-2, value-2)
...

One constraint per line and each constraint is represented in "(...)" in which each component is separated by a comma.

## Constraints
The list of constraint defined is in the file "constraints.json". You can add or modify the constraints in the file.
Here is the syntax if you want to add some constraints :
<pre><code>
"key of constraint (for example for string, it is 'string', etc... ") : {
	"arguments" : [integer] Number of arguments used for the constraint.
	"constraints" : [String] Represents an array of mathematical formulation of your constraints with the respective variables (x1, x2, ..., xn) where n is the number of arguments for example, ['x1 < x2', 'x2 < x3'] for a constraint with 3 variables. The maximum of variables for each element of the array is 2. Look in the json for the between and chain the construction of an array of constraint
	"indices" (optional if you have 1 argument) : [String] Corresponds of an 2-D array in which each subarray contains the indices of variables used in each constraint defined in "constraints" section. For example,  if you're constraint is "['x1 < x2', 'x2 < x3']", you will have in indices : "[[1,2], [2,3]]".
	"comment" (optional) : [String] comment of the constraints. Express what the constraint represent in a formal formulation.
}
</code></pre>

Some semantic representations are provided. You can use those following semantics representations (not necessary all of them) but
more you define the constraints more precise the solution will be :
* (string, var-1, value-1) : define a variable and the value of variable.
* (first, var-1) : the variable needs to be the first word of the sentence.
* (last, var-1) : the variable needs to be the last word of the sentence.

* (meets, var-1, var-2) : The variable "var-1" needs to be DIRECTLY before the variable "var-2" in the sentence.
* (precedes, var-1, var-2) : The variable "var-1" needs to before the variable "var-2" in the sentence.
* (next, var-1, var-2) : The variable "var-1" needs to be DIRECTLY after the variable "var-2".
* (follows, var-1 , var-2) : The variable "var-1" needs to be after the variable "var-2" in the sentence.

* (between, var-1, var-2, var-3) : The variable var-2 needs to be between var-1 and var-3.

* (chain, var-1, var-2, var-3, var-4) : Represent a sequence of ordering words in which each pair (defined in json) respects the precedence relation.
                                        You can change the order of the words if you want in the json file.