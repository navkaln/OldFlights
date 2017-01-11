from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import csv

#with open("AirportPopularity.csv", "r") as csvfile:

def get_more_info(airport):
    with open("OpenAirportsDB.csv", "r", newline = "", encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[13] == airport.upper():
                return(row)
        return("Error")

def get_airport_coords(airport):
    AirportData = get_more_info(airport)
    if AirportData == "Error":
        return "Error"
    #print((AirportData[4], AirportData[5]), airport)
    AirportCoords = (AirportData[4], AirportData[5])
    return AirportCoords


def create_airport_coords_csv():
    with open("PopularAirportCoords.csv", "w", newline = "", encoding='utf-8') as csvfile:
        errors = []
        writenew = csv.writer(csvfile)
        with open("AirportPopularityOrdered.csv", "r", newline = "", encoding='utf-8') as readfile:
            AirPop = csv.reader(readfile)
            for row in AirPop:
                if int(row[1]) >= 0:
                    airport = row[0].upper()
                    coords = get_airport_coords(airport)
                    if coords != "Error":
                        writenew.writerow([airport, row[1], coords[0], coords[1]])
                    else:
                        writenew.writerow([airport, row[1]])
                        errors.append(airport)


def get_airport_zones(airport):
    with open("OpenAirportsDB.csv", "r", newline="",encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            #print(airport, row[13])
            if airport == row[13]:
                #print("found zone")
                zone = row[9]
                return zone
        return "Error"


def create_airport_zones_csv():
    with open("PopularAirportCoordsZones.csv", "w", newline = "", encoding='utf-8') as csvfile:
        errors = []
        writenew = csv.writer(csvfile)
        with open("PopularAirportCoords.csv",'r',newline="",encoding='utf-8') as readfile:
            AirPopCoords= csv.reader(readfile)
            for row in AirPopCoords:
                if int(row[1]) >= 0:
                    airport = row[0]
                    zone = get_airport_zones(airport)
                    if zone != "Error":
                        #print(airport)
                        writenew.writerow([airport, row[1], row[2], row[3], zone])
                    else:
                        writenew.writerow([airport, row[1], row[2], row[3],""])
                        errors.append(airport)
        #print(errors)
    print("finished")


def get_distance(origin,destination):
    with open("PopularAirportCoords.csv", "r", newline="", encoding = "utf-8") as csvfile:
        a = 0
        b = 0
        csvreader = csv.reader(csvfile)
        while(a == 0 and b == 0):
            for row in csvreader:
                if origin == row[0].upper():
                    a = (row[2], row[3])
                elif destination == row[0].upper():
                    b = (row[2], row[3])

        return great_circle(a,b).miles

def in_same_zone(airport):
    with open("PopularAirportCoordsZones.csv", "r", newline = "", encoding='utf-8') as csvfile:
        list = []
        reader = csv.reader(csvfile)
        for rowa in reader:
            if airport == rowa[0]:
                #print(rowa)
                zone = rowa[4]
                for rowb in reader:
                    #print(rowb)
                    if zone == rowb[4] and int(rowb[1]) > 15:
                        print(rowb)
                        list.append(rowb[0])
                return list

