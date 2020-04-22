##REMEMBER TO COMMENT THIS
filein = "temp.txt"
fileout = "sudo_in.txt"
def readin():
    f = open(filein, "r")
    lines = f.readlines()
    f.close()
    f = open(fileout, "w")
    # remove the lines that cannot contain numbers (i.e. the puzzle borderlines) 
    for i in range(0,12,3):
        del lines[i]
    row = col = 1
    for i in lines:
        col = 1
        for j in i:
            if j == '*' or j.isdigit():
                if j.isdigit():
                    # Writing to the sudo_in file
                    f.writelines("%s %d %d\n" % (j, row, col))
                col += 1
        row += 1        
    f.close()


readin()
