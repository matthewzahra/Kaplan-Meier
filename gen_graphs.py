import matplotlib.pyplot as plt
'''
Takes survival data and plots curve(s) - step curve, position = "post"
Takes various info from user, such as a title and option for grid lines
'''
def plotPoints(survivalData):#survivalData is an list of tuples (timeStamp, chance of surviving)
    #add in point (0,1) as at time 0, everyone is alive
    xPoints = [0]
    yPoints = [1]

    for entry in survivalData:
        xPoints.append(entry[0])#time on x-axis
        yPoints.append(entry[1])#chance of surviving on y-axis

    plt.step(xPoints,yPoints,where="post")#steps are post rather than pre


def genGraph(survivalData,legendTitles):
    for entry in survivalData:
        plotPoints(entry)

    plt.legend(legendTitles)#legend titles

    plt.title(input("Enter title>>> "))

    grid = input("Grid lines y/n? ")
    if grid == "y":
        plt.grid()

    plt.xlabel("Time (months)")
    plt.ylabel("Survival")    
    plt.show()