'''
Reads the data from a specified file
Sorts data by a given header
Deletes any necessary results (user specified)
Can split data by a specific column
'''
def read_data(fname): #returns a 2D array (array of arrays) containing everything in the csv file
    f = open(fname, "r")
    data = []
    text = f.read().split("\n")[:-1] #removes last element as it splits on \n so last is blank
    for line in text:
        data.append(line.split(","))

    return data

def find_col_index(arr,header): #finds index value of a certain column - !!! breaks if invalid column name is entered
    for i in range(len(arr)):
        if arr[0][i] == header:
            return i

def removeNonNumbers(arr,headerIndex):#deletes all entries where the follow up column doesn't have a number - so non-numbers and blank entries are removed
    index = 0
    for entry in arr:
        try:
            int(arr[index][headerIndex])
            index += 1
        except:
            del arr[index]
    return arr

def sort(arr,header): #sorts all patients from smallest to highest by sorting them via a specified column
    headerIndex = find_col_index(arr,header)
    headerNames = arr[0] #removes titles for later
    arr = arr[1:]
    arr = removeNonNumbers(arr,headerIndex) #remove all non number values (such as blank entries) for follow up time column
    for i in range(1,len(arr)):
        index = i
        insert = int(arr[i][headerIndex])
        insertRow = arr[i] #save whole patient row for swap
        while index > 0 and insert < int(arr[index-1][headerIndex]):
            arr[index] = arr[index-1] #replace entire patient row
            index -= 1
        arr[index] = insertRow #replace entire patient row
    arr.insert(0,headerNames) #adds titles back on
    return arr

def deleteValues(arr,headerToDelete,valueToDelete):#given a column header, it can delete all records that have a specific value - e.g., from Radical/Adjuvant column, delete all records with an ADJUVANT entry
    headerToDeleteIndex = find_col_index(arr,headerToDelete)
    headers = arr[0]
    arr = arr[1:]
    newArr = [headers]
    for i in range(len(arr)):
        if not(arr[i][headerToDeleteIndex] == valueToDelete):
            newArr.append(arr[i])
    return newArr

def splitData(arr):#splits data by a column
    header = input("Enter the header to split by>>> ")
    noOfValues = int(input("How many different values do you want to split by?>>> "))
    values = []
    legendTitles = []

    for i in range(noOfValues):#gets values to split by and values to put into legend on graph
        values.append(input("Enter value {}>>> ".format(i + 1)).upper())
        legendTitles.append(input("Enter the legend title for this value>>> "))

    headerIndex = find_col_index(arr,header)
    newData = []

    for i in range(noOfValues):
        extractedValues = [arr[0]]#headers
        for j in range(len(arr)):
            if str(arr[j][headerIndex]).upper() == values[i]:#do splitting
                extractedValues.append(arr[j])
        newData.append(extractedValues)
    return newData,legendTitles


def get_and_sort(fname,header,split): #using functions above to extract data and sort it by a specific column
    data = read_data(fname) #extracts data into a list from sepcified file
    data = sort(data,header) #sorts patients by specified column name

    #Deletes all records that have a specified value in a specified column
    delete = input("Delete values y/n? ")
    while delete == "y":
        headerToDelete = input("Enter column header to delete from>>> ")
        valueToDelete = input("Enter value to delete>>> ")
        data = deleteValues(data,headerToDelete,valueToDelete)
        delete = input("Delete more values y/n? ")

    if split:#turns data into an array of arrays, each one being one of the different values it was split by - this produces multiple curves
        data,legendTitles = splitData(data)
    else:
        data = [data]#if the data is not split - so there is 1 curve, still need an array of arrays, just an array inside an array here - needed for later indexing
        legendTitles = ""
    return data,legendTitles