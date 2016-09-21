
from math import radians, cos, sin, asin, sqrt
try:
    import problem1.vincenty as vincenty
except Exception:
    import vincenty as vincenty


class routeSegment:
    'Object for holding the route between two nodes'
    separator = '|'
    source = ""
    goal = ""
    def __init__(self,destination,route_string,miles,duration,highway_string):
        #self.source = source
        self.destination = destination
        self.route_string = route_string
        self.miles = miles
        self.duration = duration #in minutes
        self.highway_string = highway_string
        self.level = len(self.route_string.split(self.separator)) - 1
        #Change here to test with different heuristic implementations
        self.est_distance = self.euclidean()#self.vincenty()#self.haversine()

    def __eq__(self, other):
        if other == None:
            return False
        return self.miles == other.miles

    def __lt__(self, other):
        if self.source.name == self.destination.name:
            return False
        elif other.source.name == other.destination.name:
            return True
        return self.miles < other.miles

    def machine_readable_stringify(self):
        #Prints the object in a machine readable format
        print("%d %s %d %s" %(self.miles, self.format_minutes(),self.level,self.route_string))

    def format_minutes(self):
        minutes = self.duration
        if(minutes < 60):
            return "%d minutes" %minutes
        hours = minutes/60
        minutes = hours % 60
        if minutes == 0:
            return "%d Hours" %(hours)
        return "%d Hours, %d Minutes" %(hours,minutes)

    def human_readable_stringify(self):
        print("Print human readable solution")

    def euclidean(self):
        lat1 = self.goal.lat
        lat2 = self.goal.lon
        lon1 = self.destination.lat
        lon2 = self.destination.lon
        square_distance = (lat2 - lat1)**2 + (lon2 - lon1)**2
        return sqrt(square_distance)
	
	#Source: http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    def haversine(self):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        lat1 = self.goal.lat
        lat2 = self.goal.lon
        lon1 = self.destination.lat
        lon2 = self.destination.lon
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km
	#Vincenty distance formula implementation done by the library (source code uploaded along with the submission)
	#Link : https://pypi.python.org/pypi/vincenty/0.1.4
    def vincenty(self):
        lat1 = self.goal.lat
        lat2 = self.goal.lon
        lon1 = self.destination.lat
        lon2 = self.destination.lon
        return vincenty.vincenty((lat1,lon1),(lat2,lon2),True)


class City:

    def __init__(self,name,lat,lon):
        self.name = name
        self.lat = float(lat)
        self.lon = float(lon)


