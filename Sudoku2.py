"""
The Looping Sudoku Problem Formulation for the PuLP Modeller

Authors: Antony Phillips, Dr Stuart Mitcehll

Edited by: Kara Batson, Evan Branyon and Chelsea Menenzes
"""
# Import PuLP modeler functions
from pulp import *

## File reading name. Note: this file must exist in current directory
filename = "sudo_in.txt"

# A list of strings from "1" to "9" is created
Sequence = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

# The Vals, Rows and Cols sequences all follow this form
Vals = Sequence
Rows = Sequence
Cols = Sequence

# The boxes list is created, with the row and column index of each square in each box
Boxes =[]
for i in range(3):
    for j in range(3):
        Boxes += [[(Rows[3*i+k],Cols[3*j+l]) for k in range(3) for l in range(3)]]

# The prob variable is created to contain the problem data        
prob = LpProblem("Sudoku Problem",LpMinimize)

# The problem variables are created
choices = LpVariable.dicts("Choice",(Vals,Rows,Cols),0,1,LpInteger)

# The arbitrary objective function is added
prob += 0, "Arbitrary Objective Function"

# A constraint ensuring that only one value can be in each square is created
for r in Rows:
    for c in Cols:
        prob += lpSum([choices[v][r][c] for v in Vals]) == 1, ""

# The row, column and box constraints are added for each value
for v in Vals:
    for r in Rows:
        prob += lpSum([choices[v][r][c] for c in Cols]) == 1,""
        
    for c in Cols:
        prob += lpSum([choices[v][r][c] for r in Rows]) == 1,""

    for b in Boxes:
        prob += lpSum([choices[v][r][c] for (r,c) in b]) == 1,""
                        
# The starting numbers are entered as constraints                
# NOTE: A puzzle with incomplete clues can have more than one solution
#TEST
##prob += choices["3"]["1"]["3"] == 1,""
##prob += choices["1"]["1"]["7"] == 1,""
##prob += choices["6"]["1"]["8"] == 1,""
##prob += choices["9"]["1"]["9"] == 1,""
##prob += choices["1"]["2"]["1"] == 1,""
##prob += choices["2"]["2"]["2"] == 1,""
##prob += choices["7"]["2"]["7"] == 1,""
##prob += choices["4"]["3"]["2"] == 1,""
##prob += choices["5"]["3"]["6"] == 1,""
##prob += choices["5"]["4"]["2"] == 1,""
##prob += choices["2"]["4"]["5"] == 1,""
##prob += choices["9"]["4"]["7"] == 1,""
##prob += choices["3"]["5"]["6"] == 1,""
##prob += choices["7"]["5"]["8"] == 1,""
##prob += choices["2"]["6"]["1"] == 1,""
##prob += choices["5"]["6"]["4"] == 1,""
##prob += choices["9"]["6"]["5"] == 1,""
##prob += choices["4"]["6"]["6"] == 1,""
##prob += choices["8"]["7"]["1"] == 1,""
##prob += choices["3"]["7"]["5"] == 1,""
##prob += choices["6"]["7"]["6"] == 1,""
##prob += choices["4"]["8"]["3"] == 1,""
##prob += choices["5"]["8"]["7"] == 1,""
##prob += choices["6"]["9"]["1"] == 1,""
##prob += choices["8"]["9"]["8"] == 1,""


## Read the file inputs for choices
rfile = open(filename)
while lines := rfile.readline():
    num = [x.strip(' ') for x in lines]
    ## Seperates by spaces, every 2 elements
    prob += choices[num[0]][num[2]][num[4]] == 1,""
rfile.close()


# The problem data is written to an .lp file
prob.writeLP("Sudoku.lp")

# A file called sudokuout.txt is created/overwritten for writing to
sudokuout = open('sudokuout.txt','w')

while True:
    prob.solve()
    # The status of the solution is printed to the screen
    print ("Status:", LpStatus[prob.status])
    # The solution is printed if it was deemed "optimal" i.e met the constraints
    if LpStatus[prob.status] == "Optimal":
        # The solution is written to the sudokuout.txt file 
        for r in Rows:
            if r == "1" or r == "4" or r == "7":
                print("+-------+-------+-------+")
                sudokuout.write("+-------+-------+-------+\n")
            for c in Cols:
                for v in Vals:
                    if value(choices[v][r][c])==1:
                        if c == "1" or c == "4" or c =="7":
                            print("| ", end='')
                            sudokuout.write("| ")
                        print(v + " ", end='')
                        sudokuout.write(v + " ")
                        if c == "9":
                            print("|")
                            sudokuout.write("|\n")
        print("+-------+-------+-------+", end="\n\n")
        sudokuout.write("+-------+-------+-------+\n\n")
        # The constraint is added that the same solution cannot be returned again
        prob += lpSum([choices[v][r][c] for v in Vals
                                        for r in Rows
                                        for c in Cols
                                        if value(vars[v][r][c])==1]) <= 80
    # If a new optimal solution cannot be found, we end the program    
    else:
        break
sudokuout.close()

# The location of the solutions is give to the user
print ("Solutions Written to sudokuout.txt")

