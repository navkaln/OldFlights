import requests
import json
from skyscanner import Flights
import os.path
import geograph
import csv
import datetime
import ThirdLeg


#default values
originplace = "nyc"
country = "UK"
currency = "USD"
locale = "en-US"
locationSchema = "iata"
grouppricing = "on"
destinationplace = ""
outbounddate = ""
inbounddate = ""
adults = "1"
children = "0"
infants = "0"
carriernumber = ""
cabinclass = "Economy"
price = "0"
carriername = ""
apikey = '<your API key>'
errors = "graceful"
narrowSearch = "anywhere"



def get_cache(originplace, country = "US", currency = "USD", locale = "en-US", narrowSearch="anywhere"):
    #requests cached data on SkyScanner for flights and writes
    print("requesting")
    r = requests.get("http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/" + country + "/" + currency + "/" + locale + "/" + originplace + "/" + narrowSearch + "/anytime/anytime?apiKey=" + apikey)
    print("requested")
    with open('flightdata.js', 'w') as outfile:
        json.dump(r.json(), outfile, sort_keys=True, indent=4,)

def get_all_cache(minpopularity, region="anywhere", daysold=24, cpm=100, narrowSearch="anywhere"):
    """
    Uses list of airports (listed by popularity) to search for flights departing there
    to anywhere.
    :param minpopularity: minpopularity will limit search to airports of a minimum
      popularity, such that if the airport isn't searched frequently as a departing
      airport, it won't be included
    """
    #gets datetime of oldest search being returned
    oldest = datetime.datetime.now()-datetime.timedelta(days=daysold)
    with open("PopularAirportCoordsZones.csv", "r", newline = "", encoding='utf-8') as f:
        AirportReader = csv.reader(f) # each row contains airport with corresponding lat/long and ISO zone

        for row in AirportReader:
            if (region == "anywhere" or row[4].startswith(region)) and (int(minpopularity) < int(row[1])):
                print(row)
                #searchs SkyScanner API for flights matching parameters & stores in flightdata.js
                get_cache(row[0],narrowSearch=narrowSearch)

                #reads flightdata.js and reads each historical quote
                with open('flightdata.js') as inputfile:
                    d = json.load(inputfile)
                    #currency = d["Currencies"][0]["Code"]
                    for quote in d["Quotes"]:
                        #print(quote)
                        outbounddate = quote["OutboundLeg"]["DepartureDate"][:10]
                        inbounddate = quote["InboundLeg"]["DepartureDate"][:10]
                        originplace = quote["OutboundLeg"]["OriginId"]
                        destinationplace = quote["InboundLeg"]["OriginId"]
                        price = quote["MinPrice"]
                        QuoteId = quote["QuoteId"]
                        Direct = quote["Direct"]
                        QDT = quote["QuoteDateTime"]
                        QuoteDateTime = datetime.datetime(int(QDT[:4]), int(QDT[5:7]), int(QDT[8:10]), int(QDT[11:13]),
                                                          int(QDT[14:16]), int(QDT[17:19]))
                        if quote["OutboundLeg"]["CarrierIds"] == []:
                            carriernumber = ""
                        else:
                            carriernumber = quote["OutboundLeg"]["CarrierIds"][0]

                        # Grabs origin and destination from index at top of json file
                        for place in d["Places"]:
                            if place["PlaceId"] == destinationplace:
                                # print("DestMatch")
                                destinationplace = place["IataCode"]
                            elif place["PlaceId"] == originplace:
                                # print("OrigMatch")
                                originplace = place["IataCode"]

                        # Grabs carrier name if exists
                        if carriernumber != "":
                            for carrier in d["Carriers"]:
                                if carriernumber == carrier["CarrierId"]:
                                    # print("CarrieMatch")
                                    carriername = carrier["Name"]
                        else:
                            carriername = "Unknown Airline"

                        #calculates total distance and cents per mile
                        distance = geograph.get_distance(originplace, destinationplace)
                        centspermile = (50*price / distance)

                        #if quote matches parameters, dumps flight to csv
                        if centspermile < cpm and oldest < QuoteDateTime and carriername != "Wizz Air":
                            with open ("flightsdump.csv", "a", newline="", encoding='utf-8') as g:
                                GoogleLink = ThirdLeg.googleroundtrip(originplace, destinationplace, outbounddate,
                                                                      inbounddate)
                                MomoLink = ThirdLeg.momondoroundtrip(originplace, destinationplace, outbounddate,
                                                                      inbounddate)
                                print("dumping",QuoteId,originplace,outbounddate,destinationplace,inbounddate,price,GoogleLink,MomoLink)
                                flightsdump = csv.writer(g)
                                flightsdump.writerow([carriername,originplace,destinationplace,outbounddate,inbounddate,QuoteDateTime,Direct,price,distance,centspermile,row[4],GoogleLink,MomoLink])

def grab_repo(daysOld=2,cpm=10):
    with open("flightsdumprepo.csv","r",newline="",encoding='utf-8') as d:
        readfile = csv.reader(d)
        for row in readfile:
            if row[0] == 1:
                print(row)

def get_regional_cache(minpopularity, region, daysold=24, cpm=100, narrowSearch="anywhere"):
    """
    Uses list of airports (listed by popularity) to search for flights departing there
    to anywhere.
    :param minpopularity: minpopularity will limit search to airports of a minimum
      popularity, such that if the airport isn't searched frequently as a departing
      airport, it won't be included
    :return:
    """
    now = datetime.datetime.now()
    maxage = datetime.timedelta(days=daysold)
    oldest = now - maxage
    with open("PopularAirportCoordsZones.csv", "r", newline="", encoding='utf-8') as f:
        AirportReader = csv.reader(f)
        for row in AirportReader:
            if int(minpopularity) < int(row[1] and region == row[4][:2]):
                print(row)
                get_cache(row[0], narrowSearch=narrowSearch)
                with open('flightdata.js') as inputfile:
                    d = json.load(inputfile)
                    # currency = d["Currencies"][0]["Code"]
                    for quote in d["Quotes"]:
                        # print(quote)
                        outbounddate = quote["OutboundLeg"]["DepartureDate"][:10]
                        inbounddate = quote["InboundLeg"]["DepartureDate"][:10]
                        originplace = quote["OutboundLeg"]["OriginId"]
                        destinationplace = quote["InboundLeg"]["OriginId"]
                        price = quote["MinPrice"]
                        QuoteId = quote["QuoteId"]
                        Direct = quote["Direct"]
                        QDT = quote["QuoteDateTime"]
                        QuoteDateTime = datetime.datetime(int(QDT[:4]), int(QDT[5:7]), int(QDT[8:10]), int(QDT[11:13]),
                                                          int(QDT[14:16]), int(QDT[17:19]))
                        if quote["OutboundLeg"]["CarrierIds"] == []:
                            carriernumber = ""
                        else:
                            carriernumber = quote["OutboundLeg"]["CarrierIds"][0]

                        # Grabs origin and destination from index at top of json file
                        for place in d["Places"]:
                            if place["PlaceId"] == destinationplace:
                                # print("DestMatch")
                                destinationplace = place["IataCode"]
                            elif place["PlaceId"] == originplace:
                                # print("OrigMatch")
                                originplace = place["IataCode"]

                        # Grabs carrier name if exists
                        if carriernumber != "":
                            for carrier in d["Carriers"]:
                                if carriernumber == carrier["CarrierId"]:
                                    # print("CarrieMatch")
                                    carriername = carrier["Name"]
                        else:
                            carriername = "Unknown Airline"

                        distance = geograph.get_distance(originplace, destinationplace)
                        centspermile = (50 * price / distance)

                        if centspermile < cpm and oldest < QuoteDateTime:
                            with open("flightsdump.csv", "a", newline="", encoding='utf-8') as g:
                                print("dumping", QuoteId, originplace, destinationplace, QuoteDateTime)

                                flightsdump = csv.writer(g)
                                flightsdump.writerow(
                                    [carriername, originplace, destinationplace, outbounddate, inbounddate,
                                     QuoteDateTime, Direct, price, distance, centspermile])


def find_live_flights():
    """
    Finds flights that are still alive in flightdata.js
    :return:
    """
    with open('flightdata.js') as inputfile:
        d = json.load(inputfile)
        currency = d["Currencies"][0]["Code"]
        for quote in d["Quotes"]:
            #print(quote)
            outbounddate = quote["OutboundLeg"]["DepartureDate"][:10]
            inbounddate = quote["InboundLeg"]["DepartureDate"][:10]
            originplace = quote["OutboundLeg"]["OriginId"]
            destinationplace = quote["InboundLeg"]["OriginId"]
            price = quote["MinPrice"]
            QuoteId = quote["QuoteId"]
            if quote["OutboundLeg"]["CarrierIds"] == []:
                carriernumber = ""
            else:
                carriernumber = quote["OutboundLeg"]["CarrierIds"][0]

            #Grabs origin and destination from index at top of json file
            for place in d["Places"]:
                if place["PlaceId"] == destinationplace:
                    #print("DestMatch")
                    destinationplace = place["IataCode"]
                elif place["PlaceId"] == originplace:
                    #print("OrigMatch")
                    originplace = place["IataCode"]

            #Grabs carrier name if exists
            if carriernumber != "":
                for carrier in d["Carriers"]:
                    if carriernumber == carrier["CarrierId"]:
                        #print("CarrieMatch")
                        carriername = carrier["Name"]
            else:
                carriername = "Unknown Airline"

            distance = geograph.get_distance(originplace, destinationplace)
            print(QuoteId, carriername, carriernumber, originplace, destinationplace, outbounddate, inbounddate, currency, price, distance, (50*price / distance), "cpm")

            if os.path.exists('data%s%s%s.js' % (originplace, destinationplace, price)):
                #if file exists, prints cheapest price
                with open('data%s%s%s.js' % (originplace, destinationplace, price), 'r') as inputfile:
                    live = json.load(inputfile)
                    print(live["Itineraries"][0]["PricingOptions"][0]["Price"])
                    for deeplink in live["Itineraries"][0]["PricingOptions"]:
                        if (deeplink["Price"] < price*1.1):
                            print(deeplink["DeeplinkUrl"])
                            print(deeplink["Price"])#Current cheapest prices

            if not os.path.exists('data%s%s%s.js' % (originplace, destinationplace, price)):
                #searches live pricing API
                flights_service = Flights(apikey)

                result = flights_service.get_result(
                    country = country,
                    currency = currency,
                    locale = locale,
                    locationSchema = locationSchema,
                    grouppricing = grouppricing,
                    originplace = originplace,
                    destinationplace = destinationplace,
                    outbounddate = outbounddate,
                    inbounddate = inbounddate,
                    adults = adults,
                    children = children,
                    infants = infants,
                    #carrierschema = "iata",
                    cabinclass = cabinclass,
                    errors="GRACEFUL").parsed

                #print(result)
                with open('data%s%s%s.js' % (originplace, destinationplace, price), 'w') as outfile:
                    json.dump(result, outfile, sort_keys=True, indent=4,)

                #prints latest price found
                with open('data%s%s%s.js' % (originplace, destinationplace, price), 'r') as inputfile:
                    live = json.load(inputfile)
                    print(live["Itineraries"][0]["PricingOptions"][0]["Price"])
                    for deeplink in live["Itineraries"][0]["PricingOptions"]:
                        if (deeplink["Price"] < price*1.1):
                            print(deeplink["DeeplinkUrl"])
                            print(deeplink["Price"])#Current cheapest prices

def check_live(originplace, destinationplace, outbounddate,inbounddate):
    # searches live pricing API
    flights_service = Flights(apikey)

    result = flights_service.get_result(
        country=country,
        currency=currency,
        locale=locale,
        locationSchema=locationSchema,
        grouppricing=grouppricing,
        originplace=originplace,
        destinationplace=destinationplace,
        outbounddate=outbounddate,
        inbounddate=inbounddate,
        adults=adults,
        children=children,
        infants=infants,
        # carrierschema = "iata",
        cabinclass=cabinclass,
        errors="GRACEFUL").parsed

    print(len(result["Itineraries"]))
    print(result["Itineraries"][0]["PricingOptions"][0]["Price"])
    for deeplink in result["Itineraries"][0]["PricingOptions"]:
        print(deeplink["DeeplinkUrl"])
        print(deeplink["Price"])  # Current cheapest prices
    for section in result["Itineraries"]:
        print (section)



