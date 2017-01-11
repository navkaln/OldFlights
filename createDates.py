import datetime

now = datetime.datetime.now()
today = now.replace(hour=0, minute=0, second=0, microsecond=0)
tomorrow = today + datetime.timedelta(days=1)
twoweeks = datetime.timedelta(days=14)
searchrange = tomorrow + datetime.timedelta(days=320)
DaySearchOrder = [          # where Monday is 0 and Sunday is 6
    [0, 1, 2, 3, 4, 6, 5],  # Monday (0) search order
    [1, 0, 2, 3, 4, 6, 5],  # Tuesday (1) search order
    [2, 1, 3, 0, 4, 6, 5],  # etc...
    [3, 2, 4, 1, 0, 6, 5],  # Logic is keep search to adjacent days
    [4, 3, 2, 1, 0, 6, 5],  # And go to the cheaper day when possible
    [5, 6, 4, 0, 3, 1, 2],
    [6, 5, 4, 0, 3, 1, 2]]
OrdinalWithinWeek = [           # Translated into Ordinal format and zeroed at each day
    [0, 1, 2, 3, -3, -1, -2],   # Monday's search order
    [0, -1, 1, 2, 3, -3, -2],   # Tuesday's search order
    [0, -1, 1, -2, 2, -3, 3],   # Wednesday's
    [0, -1, 1, -2, -3, 3, 2],   # Thurs
    [0, -1, -2, -3, 3, 2, 1],   # etc...
    [0, 1, -1, 2, -2, 3, -3],
    [0, -1, -2, 1, -3, 2, 3]]
OrdinalOutsideWeek = [          # OutsideWeek search pattern
    [0, 7,-7, 14, -14,-6, 8],   # Monday
    [0, 7,-7, 14, -14,-6, 6],   # Tues
    [0, 7,-7, 14, -14,-6, 6],
    [0, 7,-7, 14, -14,-6, 6],
    [0, 7,-7, 14, -14, 6,-8],
    [0, 7,-7, 14, -14,-6, 8],
    [0, 7,-7, 14, -14, 6,-8]]
OrdinalWDWE = [                 # Switches WDs to WEs.
    [0,-1,-2, 5, 6, -8,-9],     # Monday
    [0,-2,-3, 4, 5,-9,-10],     # Tues
    [0,-3, 3,-4, 4,-10,10],
    [0, 2, 3,-4, -5, 9,10],
    [0, 1, 2,-5, -6, 8, 9],
    [0,-1,-2, 2, -3, 3,-4],
    [0, 1, 2,-2, 3, -3, 4]]
Decoded = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2), (3, 0), (2, 1), (1, 2), (0, 3), (4, 0), (3, 1), (2, 2), (1, 3), (0, 4), (5, 0), (4, 1), (3, 2), (2, 3), (1, 4), (0, 5), (6, 0), (5, 1), (4, 2), (3, 3), (2, 4), (1, 5), (0, 6), (6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6), (6, 2), (5, 3), (4, 4), (3, 5), (2, 6), (6, 3), (5, 4), (4, 5), (3, 6), (6, 4), (5, 5), (4, 6), (6, 5), (5, 6), (6, 6)]
"""
def CreateDecoded(q):
    #Creates cartesian product with order I need
    #Order keeps search as narrow as possible
    x = 0
    y = 0
    Decoded = []
    for n in range(2*q-1):
        x=n
        y=0
        while(x >= 0):
            if(x <= q-1 and y <= q-1):
                Decoded.append((x,y))
            x-=1
            y+=1
    return Decoded
Decoded = CreateDecoded(7)
print(Decoded)
"""

def DoW(day):
    return day.timetuple()[6]
def isWD(day):
    if (day.timetuple()[6] < 5):
        return True
    else:
        return False
def isWE(day):
    if (day.timetuple()[6] in [5,6]):
        return True
    else:
        return False

def get_weekday_dist(searches_in_month):
    """
    When initial fare occurs on both weekend or weekday dates, distributes searches into categories:
    Searching within a week of initial fare
    Searching outside that week
    Searching on both day-types (one weekend, one weekday)
    Searching on opposite day-type of initial fare (both weekend/weekday)
    """
    WithinWeek = searches_in_month // 2
    OutsideWeek = searches_in_month // 6
    OneWDayWEnd = searches_in_month // 6
    BothWDayWends = searches_in_month // 6
    r = searches_in_month - (WithinWeek + OutsideWeek + OneWDayWEnd + BothWDayWends)
    if (r == 1):
        OutsideWeek += 1
    elif (r == 2):
        OutsideWeek += 1
        WithinWeek += 1
    elif (r == 3):
        OutsideWeek += 1
        WithinWeek += 1
        OneWDayWEnd += 1

    return (WithinWeek, OutsideWeek, OneWDayWEnd, BothWDayWends)

def create_pairs(coord1, coord2, day1, day2, searches_in_month):
    """
    Uses Decoded to order searches
    """
    allsearches = []
    L1 = [OrdinalWithinWeek[day1][i]+coord1 for i in range(len(OrdinalWithinWeek[day1]))]
    L2 = [OrdinalWithinWeek[day2][i]+coord2 for i in range(len(OrdinalWithinWeek[day2]))]
    WithinWeekPairs = []
    for n in Decoded:
       WithinWeekPairs.append((L1[n[0]], L2[n[1]]))

    L1 = [OrdinalOutsideWeek[day1][i]+coord1 for i in range(len(OrdinalOutsideWeek[day1]))]
    L2 = [OrdinalOutsideWeek[day2][i]+coord2 for i in range(len(OrdinalOutsideWeek[day2]))]
    OutsideWeekPairs = []
    for n in Decoded:
        OutsideWeekPairs.append((L1[n[0]], L2[n[1]]))

    L1 = [OrdinalWithinWeek[day1][i]+coord1 for i in range(len(OrdinalWithinWeek[day1]))]
    L2 = [OrdinalWDWE[day2][i]+coord2 for i in range(len(OrdinalWDWE[day2]))]
    L3 = [OrdinalWDWE[day1][i]+coord1 for i in range(len(OrdinalWDWE[day1]))]
    L4 = [OrdinalWithinWeek[day2][i]+coord2 for i in range(len(OrdinalWithinWeek[day2]))]
    OneWDWESwitchPairs = []
    for n in Decoded:
        OneWDWESwitchPairs.append((L1[n[0]], L2[n[1]]))
        OneWDWESwitchPairs.append((L3[n[0]], L4[n[1]]))

    L1 = [OrdinalWDWE[day1][i]+coord1 for i in range(len(OrdinalWDWE[day1]))]
    L2 = [OrdinalWDWE[day2][i]+coord2 for i in range(len(OrdinalWDWE[day2]))]
    WDSwitchWEPairs = []
    for n in Decoded:
       WDSwitchWEPairs.append((L1[n[0]], L2[n[1]]))


    searches = get_weekday_dist(searches_in_month)
    WithinWeek = searches[0]
    OutsideWeek = searches[1]
    OneWDayWEnd = searches[2]
    BothWDayWends = searches[3]

    for pair in WithinWeekPairs:
        if pair not in allsearches and tomorrow.toordinal() < pair[0] < pair[1] < searchrange.toordinal() and len(allsearches)<WithinWeek:
            allsearches.append(pair)
    for pair in OutsideWeekPairs:
        if pair not in allsearches and tomorrow.toordinal() < pair[0] < pair[1] < searchrange.toordinal() and len(allsearches)<(WithinWeek+OutsideWeek):
            allsearches.append(pair)
    for pair in OneWDWESwitchPairs:
        if pair not in allsearches and tomorrow.toordinal() < pair[0] < pair[1] < searchrange.toordinal() and len(allsearches)<(WithinWeek+OutsideWeek+OneWDayWEnd):
            allsearches.append(pair)
    for pair in WDSwitchWEPairs:
        if pair not in allsearches and tomorrow.toordinal() < pair[0] < pair[1] < searchrange.toordinal() and len(allsearches)<(WithinWeek+OutsideWeek+OneWDayWEnd+BothWDayWends):
            allsearches.append(pair)

    return allsearches

def Distant_Pairs(coord1, coord2, day1, day2, searches_outside_month):
    backwards1 = coord1 - 28
    backwards2 = coord2 - 28
    forwards1 = coord1 + 28
    forwards2 = coord2 + 28
    allsearches = []
    ForwardsMonthPairs = []
    BackwardsMonthPairs = []

    while(tomorrow.toordinal() < backwards1):
        L1 = [OrdinalWithinWeek[day1][i] + backwards1 for i in range(len(OrdinalWithinWeek[day1]))]
        L2 = [OrdinalWithinWeek[day2][i] + backwards2 for i in range(len(OrdinalWithinWeek[day2]))]
        for n in Decoded[:searches_outside_month]:
            BackwardsMonthPairs.append((L1[n[0]], L2[n[1]]))
        backwards1 -= 28
        backwards2 -= 28

    while(forwards2 < searchrange.toordinal()):
        L1 = [OrdinalWithinWeek[day1][i] + forwards1 for i in range(len(OrdinalWithinWeek[day1]))]
        L2 = [OrdinalWithinWeek[day2][i] + forwards2 for i in range(len(OrdinalWithinWeek[day2]))]
        for n in Decoded[:searches_outside_month]:
            ForwardsMonthPairs.append((L1[n[0]], L2[n[1]]))
        forwards1 += 28
        forwards2 += 28

    for pair in BackwardsMonthPairs:
        if pair not in allsearches and tomorrow.toordinal() < pair[0] < pair[1] < searchrange.toordinal():
            allsearches.append(pair)

    for pair in ForwardsMonthPairs:
        if pair not in allsearches and tomorrow.toordinal() < pair[0] < pair[1] < searchrange.toordinal():
            allsearches.append(pair)


    return allsearches






def Find_Close_Dates(outbounddate, inbounddate, searches_in_month=14, searches_outside_month = 1):
    """
    When trying to find a duplicate flight deal, this generates new dates to check that might replicate fare on other dates
    """
    AllPairs = []
    d1 = datetime.datetime.strptime(outbounddate, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(inbounddate, "%Y-%m-%d")
    print(d1, d1.strftime("%A"), d1.timetuple()[6], d2, d2.strftime("%A"), d2.timetuple()[6])
    coord1 = d1.toordinal()
    coord2 = d2.toordinal()
    ClosePairs = create_pairs(coord1, coord2, DoW(d1), DoW(d2), searches_in_month)
    DistantPairs = Distant_Pairs(coord1, coord2, DoW(d1), DoW(d2), searches_outside_month)
    for pair in ClosePairs:
        AllPairs.append(pair)
    for pair in DistantPairs:
        AllPairs.append(pair)
    return AllPairs

def find_distant_date(outbounddate, inbounddate, searches_outside_month = 1):
    d1 = datetime.datetime.strptime(outbounddate, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(inbounddate, "%Y-%m-%d")
    print(d1, d1.strftime("%A"), d1.timetuple()[6], d2, d2.strftime("%A"), d2.timetuple()[6])
    coord1 = d1.toordinal()
    coord2 = d2.toordinal()





pairs = Find_Close_Dates("2017-01-10", "2017-01-20",searches_in_month=14, searches_outside_month=1)

print(len(pairs), pairs)
for pair in pairs:
    print(datetime.datetime.fromordinal(pair[0]), datetime.datetime.fromordinal(pair[1]))
