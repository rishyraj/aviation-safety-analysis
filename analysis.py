import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

def remDup(dup):
    final_list = []
    for d in dup:
        if d not in final_list:
            final_list.append(d)

    return final_list

def convertToInt(ar):
    lst = []
    for a in ar:
        lst.append(int(float(a)))
    return lst


airline = raw_input("Enter an Airline: ")
airlineFound = False

#print(airline)

dates = []
fatalities=[]
dates_aggregate=[]
fatalities_aggregate=[]

with open('data/planecrashinfo.csv') as csvFile:
    dr = csv.DictReader(csvFile)
    for row in dr:
        fatalities_rev = row['fatalities'][:row['fatalities'].index(' ')]
        if airline in row['operator']:
            airlineFound = True 
            dates.append(row['date'][row['date'].index(', ')+2:len(row['date'])])
            if '?' not in fatalities_rev:
                fatalities.append(int(float(fatalities_rev)))
        if '?' not in fatalities_rev:
            dates_aggregate.append(row['date'][row['date'].index(', ')+2:len(row['date'])])
            fatalities_aggregate.append(int(float(fatalities_rev)))
if airlineFound:
    dates_clean = convertToInt(remDup(dates))
    dates_aggregate_clean = convertToInt(remDup(dates_aggregate))
    fatalities_clean = []
    fatalities_average = []
    
    #aggregate data
    i=0
    for year in dates_aggregate_clean:
        fat_avg = 0
        count = 1
        for dt in dates_aggregate:
            if str(year) in dt:
                fat_avg+=fatalities_aggregate[i]
                i+=1
                count+=1
        #print(fat_avg)
        fatalities_average.append(fat_avg/count)
    
    #airline data
    i=0
    for year in dates_clean:
        fat = 0
        for dt in dates:
            if str(year) in dt:
                fat+=fatalities[i]
                i+=1
        fatalities_clean.append(fat)
    print("stats:")
    print("first year:"+str(dates_clean[0]))
    print("last year:"+str(dates_clean[len(dates_clean)-1]))
    print("Highest Fatality/year:"+str(max(fatalities_clean)))
    
    plt.plot(dates_clean,fatalities_clean,'r',dates_aggregate_clean,fatalities_average,'g')
    plt.axis([dates_clean[0],dates_clean[len(dates_clean)-1],0,max(fatalities_clean)+40])
    plt.ylabel('Fatalities/year')
    plt.xlabel('Year')
    plt.title(airline+' crashes over its history compared with the average crashes per year')
    plt.legend([airline+' fatalities','Overall Average'])
    plt.show()
else:
    print("Whoops! Airline not Found!")
    print("This means that the airline has never had a fatal accident or crash, or doesn't exist in our database.")
