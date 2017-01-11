import searchings
import geograph
from geopy.distance import great_circle
import csv





searchings.get_all_cache(minpopularity=73,daysold=2)


##Gets cache for a route and checks to see if flights are still alive
#searchings.get_cache(originplace="NYC", narrowSearch="BEY")
#searchings.find_live_flights()


##checks a single flight
#searchings.check_live("LAX","DEL","2017-01-20","2017-02-19")
#searchings.grab_repo()

