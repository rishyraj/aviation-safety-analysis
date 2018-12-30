import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import csv
import json
from slugify import slugify

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


#for 2.7
#airline = raw_input("Enter an Airline: ")
#for 3.x.x
#airline = input("Enter an Airline: ")
#airlineFound = False

#print(airline)

def process(airline):
    print("started "+airline)
    airlineFound = False
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
                else:
                    fatalities.append(0)
            else:
                dates.append(row['date'][row['date'].index(', ')+2:len(row['date'])])
                fatalities.append(0)
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
        #print(len(fatalities))
        for year in dates_clean:
            fat = 0
            for dt in dates:
                if str(year) in dt:
                    fat+=fatalities[i]
                    i+=1
            fatalities_clean.append(fat)
        #print("stats:")
        #print("first year:"+str(dates_clean[0]))
        #print("last year:"+str(dates_clean[len(dates_clean)-1]))
        #print("Highest Fatality/year:"+str(max(fatalities_clean)))

        lines = plt.plot(dates_clean,fatalities_clean,'r',dates_aggregate_clean,fatalities_average,'g')
        plt.axis([dates_clean[0],dates_clean[len(dates_clean)-1],0,max(fatalities_clean)+50])
        plt.ylabel('Fatalities/year')
        plt.xlabel('Year')
        plt.title(airline+' crashes over its history compared with the average crashes per year')
        plt.legend([airline+' fatalities','Overall Average'])
        plt.gcf().set_size_inches(14.5, 10.5)
        mplcursors.cursor(lines, hover=True)
        plt.savefig('data/plots/'+slugify(airline)+'.png')
        #plt.show(lines)
        plt.gcf().clear()
        print("finished"+airline)
    else:
        print("Whoops! Airline not Found!")

        print("This means that the airline has never had a fatal accident or crash, or doesn't exist in our database.")



data = {}
airlines = []

with open('data/planecrashinfo.csv') as csvFile:
    dr = csv.DictReader(csvFile)
    for row in dr:
        if '?' not in row['operator']:
            airlines.append(row['operator'])

airlines = remDup(airlines)

amount = len(airlines)
count = 1
for airline in airlines:
    print("Started: "+str(count))
    print("# Left: "+str(amount - count))
    print("-----------")
    process(airline)
    count+=1
print("Process ended")






