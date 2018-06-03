from constraint import *
from n_grams import Bigram
import json


class Solver:
    def __init__(self, dict):
        self.dict = dict
        self.problem = Problem()
        self.variables = {}
        self.bigram = Bigram()
        self.size = len(self.dict["string"])
        with open("constraints.json") as json_file:
            self.json_data = json.loads(json_file.read())

    # Construct the problem based on the dictionnary
    # Create the problem
    # Add variables and constraints into the problem
    def construct(self):
        for key in self.dict.keys():
            if key == "string":
                self.add_variable(self.dict[key])
            else:
                self.add_constraint(key, self.dict[key])

        # Constraint : all variables need to have a different value
        self.problem.addConstraint(AllDifferentConstraint())

    # Add the variable into the problem
    def add_variable(self, list):
        # define the range of value of the variable
        # the value of the variable corresponds to the position of the word in the sentence
        range_value = [i for i in range(self.size)]
        for string_cstr in list:
            var = string_cstr[0]
            value = string_cstr[1]
            self.problem.addVariable(var, range_value)
            # add the variable and his value in array (used for transform the solution to string)
            self.variables[var] = value

    # Get the corresponding constraint in the json dict
    # Construct the lambda expression
    # Build the constraint
    def add_constraint(self, key, list):
        constr = self.json_data[key] # Get the structure of the constraint
        constr_expr = eval("lambda x1, x2: " + constr["constraint"]) # Build the lambda

        # Loop on all of stored semantic representation
        for c in list:
            # If the constraint need only 1 variable
            if int(constr["arguments"]) == 1:
                var = (c[0], c[0])
            # If the constraint need 2 variables
            else:
                var = (c[0], c[1])
            self.problem.addConstraint(constr_expr, var)

    # Solve the problem
    # Transform each solutions into a sentence
    # If there is multiple solutioon, compute the perxplexity for each sentences/solutions
    # Print the best solution with the lowest perplexity
    def solve(self):
        solutions = self.problem.getSolutions()
        if len(solutions) == 0:
            print("There is no solution.")
        elif len(solutions) == 1:
            print(self.to_string(solutions[0]))
        else:
            # Transform all solutions into sentences
            str_solutions = [self.to_string(s) for s in solutions]
            perplexity = []

            # Get the perplexity of each sentence/solution
            for s in str_solutions:
                perplexity.append(self.bigram.compute_perplexity(s))

            # Get the lowest perplexity
            min_index = perplexity.index(min(perplexity))
            print("There is multiple solutions.")
            # Print the best solution found
            print(str_solutions[min_index])

    # Transform a solution into a string
    def to_string(self, solution):
        arr_string = [i for i in range(len(solution))]
        for var, val in solution.items():
            arr_string[val] = self.variables[var]

        string = "".join(arr_string)
        return string.strip()
