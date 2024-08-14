'''
If called, writes all the survival data to a specified location
'''
def writeData(survivalResults, legendTitles):
    fname = input("Please enter a filename to write the data to (excluding the file extension)>>> ")
    fname += ".csv"
    f = open(fname,"w")

    if len(legendTitles) == 0:#if the data wasn't chosen to be split (so 1 curve), then legendTitles is blank
        legendTitles = ["survival"]
    
    index = 0
    for title in legendTitles:
        f.write("time" + "," + title + "\n")#adds in titles
        for i in range(len(survivalResults[index])):
            f.write(str(survivalResults[index][i][0]) + "," + str(round(survivalResults[index][i][1],3)) + "\n")#writes time,surivival
        index += 1
        f.write("\n")
    f.close()