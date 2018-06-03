import sys
from solver import Solver


sem_representation = {}

# Retrieve the input file in the argument of the program
if "-i" in sys.argv:
    index = sys.argv.index("-i")
    file_path = sys.argv[index+1]

f = open(file_path, "r")

for line in f.readlines():
    # remove the (, ), " and split on the comma
    tuple = line.replace("(", "").replace(")", "").replace("\"","").strip().split(",")
    type = tuple[0] # get the type of the constraint

    # If the type doesn't exist yet in the dictionnary, then create it
    if not type in sem_representation:
        sem_representation[type] = []

    # Add the argument of the semantic representation
    sem_representation[type].append(tuple[1:])

solver = Solver(sem_representation)

solver.construct()
solver.solve()

