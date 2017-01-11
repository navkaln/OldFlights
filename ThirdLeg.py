airportlist1= ("LGA","JFK","EWR","BOS")
airportlist2= ("BKK","MNL",'CGK','BOM','PNQ')
airportlist3= ('CPT','PLZ')
airportlist1= ("JFK",)
airportlist2= ("TPE",)
airportlist3= ('CPT','PLZ')

AAA = "NYC"
BBB = "PNH"
CCC = "MAA"
DDD = "JHB"
date1= "2016-12-29"
date2= "2017-01-13"
date3= "2017-05-29"


def combine_airports(airportlist1,airportlist2,airportlist3,date1,date2,date3):
    array = []
    for airport1 in airportlist1:
        for airport2 in airportlist2:
            for airport3 in airportlist3:
                array.append((airport1, date1, airport2, date2, airport3, date3))
    return array
array = combine_airports(airportlist1,airportlist2,airportlist3,date1,date2,date3)
"""
for itinerary in array:
    print(itinerary)
"""

def createFlightOne():
    return(AAA + "_" + BBB + "_" + date1)

def createFlightTwo():
    return(BBB + "_" + AAA + "_" + date2)

def createFlightThree():
    return(CCC + "_" + DDD + "_" + date3)
#print(createFlightOne(), createFlightTwo(), createFlightThree())

GoogleLink = "https://www.google.com/flights/#search;iti=FLIGHTONE*FLIGHTTWO*FLIGHTTHREE;tt=m"

GoogleLink = GoogleLink.replace("FLIGHTONE",createFlightOne())
GoogleLink = GoogleLink.replace("FLIGHTTWO",createFlightTwo())
GoogleLink = GoogleLink.replace("FLIGHTTHREE",createFlightThree())

#print(GoogleLink)
#print("https://www.google.com/flights/#search;iti=IAD_CPT_2017-02-09*CPT_IAD_2017-02-12*ADD_DSE_2017-02-19;tt=m")


def momondodate(datedate):
    newdate = ''
    newdate += datedate[8:10] + '-'
    newdate += datedate[5:7] + '-'
    newdate += datedate[:4]
    return newdate

def momondoroundtrip(origin,destination,outbounddate,inbounddate):

    MomondoRoundTripURL = 'http://www.momondo.com/flightsearch/?Search=true&TripType=2&SegNo=2&SO0=AAA&SD0=BBB&SDP0=date1&SO1=BBB&SD1=AAA&SDP1=date2&AD=1&TK=ECO&DO=false&NA=false'
    #MomondoRoundTripURL += '&source=aff-tt&utm_source=tradetracker&utm_medium=affiliate&utm_campaign=228552&utm_content=20075&utm_term=750407%3A%3A228552%3A%3A%3A%3A%3A%3A1480218825'
    MomondoRoundTripURL = MomondoRoundTripURL.replace("AAA", origin)
    MomondoRoundTripURL = MomondoRoundTripURL.replace("BBB", destination)
    MomondoRoundTripURL = MomondoRoundTripURL.replace("date1", momondodate(outbounddate))
    MomondoRoundTripURL = MomondoRoundTripURL.replace("date2", momondodate(inbounddate))
    return(MomondoRoundTripURL)


def googleroundtrip(origin,destination,outbounddate,inbounddate):
    GoogleRoundTripURL = "https://www.google.com/flights/#search;f=AAA;t=BBB;d=date1;r=date2"
    GoogleRoundTripURL = GoogleRoundTripURL.replace("AAA", origin)
    GoogleRoundTripURL = GoogleRoundTripURL.replace("BBB", destination)
    GoogleRoundTripURL = GoogleRoundTripURL.replace("date1", outbounddate)
    GoogleRoundTripURL = GoogleRoundTripURL.replace("date2", inbounddate)
    return(GoogleRoundTripURL)

"""
http://www.momondo.com/flightsearch/?Search=true&TripType=2&SegNo=2&SO0=
ABC&SD0=DEF&SDP0=
21-12-2016&SO1=
DEF&SD1=ABC&SDP1=
04-01-2017&AD=1&TK=ECO&DO=false&NA=false

"""
