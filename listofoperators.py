import csv

def remDup(dup):

    final_list = []
    for d in dup:
        if d not in final_list:
            final_list.append(d)
    return final_list


#for 2.7
#airline = raw_input("Enter an Airline: ")
#for 3.x.x
#airline = input("Enter an Airline: ")
#airlineFound = False

#print(airline)

airlines = []

with open('data/planecrashinfo.csv') as csvFile:
    dr = csv.DictReader(csvFile)
    for row in dr:
        if '?' not in row['operator']:
            airlines.append(row['operator'])

airlines = remDup(airlines)

print(airlines)






