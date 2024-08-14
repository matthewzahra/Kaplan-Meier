'''
Kaplan Meier Curve Generator - Matthew Zahra
'''
import get_data
import survival_function
import gen_graphs
import write_csv

def main():
    print('''
############################################
Kaplan Meier Curve Generator - Matthew Zahra
############################################
''')

    #gets the inputs from the user
    fname = input("Enter the name of the csv file to be examined>>> ")
    timeHeader = input("Enter the header name which contains the follow up time>>> ")
    eventHeader = input("Enter the binary header that indicates whether the event has occured (0 - event has not happened, 1 - event has happened)>>> ")
    endTime = int(input("Enter the total time frame to look at e.g. for 60 months, enter 60>>> "))
    interval = int(input("Enter the time interval to examine e.g. to look at events every 3 months, enter 3>>> "))


    split = input("Split into different groups y/n? ")
    if split == "y":
        split = True
    else:
        split = False

    data,legendTitles = get_data.get_and_sort(fname,timeHeader,split) #retrieves data from specified csv file and sorts is by a specified column name
    survivalResults = []


    if legendTitles == "":#title for printing number in each group
        titles = ["Entries"]
    else:
        titles = legendTitles

    index = 0
    for entry in data:#data is an array of arrays due to splitting
        survivalResults.append(survival_function.survival_function(entry,timeHeader,eventHeader, interval, endTime)) #passes data into survival function to get results
        print("\n{} - {}".format(titles[index],len(entry)-1))#displays the number of entries for each group, ignoring titles
        print(survivalResults[-1])#displays the survival results for each group
        index += 1


    gen_graphs.genGraph(survivalResults,legendTitles)#passes titles and results to be graphed


    csv = input("Write data to csv y/n? ")#can write results to a csv file
    if csv == "y":
        write_csv.writeData(survivalResults,legendTitles)

    print("\nFinished")



if __name__ == "__main__":
    main()