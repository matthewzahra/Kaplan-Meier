import get_data #from get_data file - using function to find index of specific header
'''
Works out survival results
One "issue" - if time is 3, interval = 3, people who are alive at time 3 are censored
if time == endTime, people who are alive at time are not censored
This is for the ease of the algorithm working, however, with a small enough interval and a big enough dataset, the margin of error should NOT have an affect
'''

#if we remove all people who are censored at time t (lost to follow up, so still alive), then everyone else before time t must have died (assuming t < endTime)
#This function removes anyone from the data who is still alive at time t
#assumes data is ordered by follow up in ascending order
#headerIndex is the column with the follow up time
#evetHeaderIndex is the column with the event binary - 0 = alive

def remove_censors(arr, time, headerIndex, eventHeaderIndex):#removes people who are lost to follow up (alive)
    for i in range(len(arr)):
        if int(arr[i][headerIndex]) > time:#as they are in order of Follow Up Time, as soon as one is beyond the time period getting examined, we can stop
            break
        elif int(arr[i][eventHeaderIndex]) == 0: #they are alive so should be censored as have only been followed for a time less than current time
            arr[i] = "C" #change row to censored status
    noCensors = []
    for row in arr: #removes all entries with censored status
        if row != "C":#remove all ones with censored status
            noCensors.append(row)
    return noCensors

def remove_events(arr, time, headerIndex): #since it is used after censors are removed, we can assume everyone before or at time t is dead (assuming time t < endTime)
    events = 0
    index = 0
    for i in range(len(arr)):
        if int(arr[i][headerIndex]) > time:
            break
        else:
            events += 1
            index += 1
    return arr[index:], events
            

def survival_function(arr, header, eventHeader, interval, endTime): #works out survivial function - eventHeader = column indicating if that patient has experinced an event, header = column name to consider, interval = gap betwen inspections, e.g. interval = 3, survival funtion looks at time = 3,6,9,12..., endTime = total time of test, e.g. stop at 60 months
    headerIndex = get_data.find_col_index(arr, header)
    eventHeaderIndex = get_data.find_col_index(arr, eventHeader)
    arr = arr[1:] #removes headers
    survival = [] #for the survival chances at each time interval

    previousTime = -1
    end = False
    for t in range(1,endTime//interval + 2): #integer division incase endTime is not divisibile by interval (everyone alive at time 0) - + 2 incase it is not evenly divisible by the integer, need time to equal or overshoot endTime at some point
        time = t * interval
        if time < endTime:#if alive at t = endTime or more, don't want to censor as they completed the whole test
            arr = remove_censors(arr, time, headerIndex, eventHeaderIndex) #once all censored individuals before time t are removed, then all the other entries before time t are deaths, assuming time t < endTime
        elif time >= endTime:#if time overshoots endtime, find out who died just before endTime - anyone who made it to endTime is considered to have survived the whole time
            time = endTime 
            time -= 1 #people who made it to the end time are considered alive, so we should not censor them nor count any of them as deaths, hence, we examine endTime - 1
            end = True
            arr = remove_censors(arr, time, headerIndex, eventHeaderIndex) #removes any censors that occur just before endTime

        atRisk = len(arr) #Number at risk is number of uncensored patients at time t BEFORE deaths are removed

        if atRisk == 0:#if the data set is incomplete - i.e. endTime = 60, but, at time = 48 there are no more entries - so survival goes unchanged
            if not(end):
                survival.append((time,survival[-1][-1]))
                continue
            else:
                survival.append((time+1,survival[-1][-1]))
                return survival
        else:
            arr, events = remove_events(arr, time, headerIndex) #removes and counts deaths (as events) and returns list without deaths that occured at time t or before and the number of deaths
            currentSurvival = 1 - (events/atRisk) #finds chance of surviving at this time
        
        if time != previousTime or end == True:#if endTime is evenly divisible by the interval, it will set endTime to endTime-1 twice - this ensures that if this happens, the same record is not appended twice
            previousTime = time
            if len(survival) == 0:
                survival.append((time,currentSurvival))
            else:
                if not(end):
                    survival.append((time,currentSurvival * survival[-1][-1])) #finds cumulative chance of surviving
                else:
                    survival.append((time+1,currentSurvival * survival[-1][-1])) #finds cumulative chance of surviving
                    return survival