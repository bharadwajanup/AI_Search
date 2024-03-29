from math import radians, cos, sin, asin, sqrt

try:
    import problem1.vincenty as vincenty
except ImportError:
    import vincenty as vincenty


class RouteNode:
    'Object for holding the route between two nodes'
    separator = '|'
    source = ""
    goal = ""

    def __init__(self, destination, route_string, miles, duration, highway_string, highway_count):
        # self.source = source
        self.destination = destination
        self.route_string = route_string
        self.miles = miles
        self.duration = duration  # in minutes
        self.highway_count = highway_count
        self.highway_string = highway_string
        self.level = len(self.route_string.split(self.separator)) - 1

    @classmethod
    def from_file(cls, line, des_index):
        parts = line.split()
        if len(parts) != 5:
            return None
        des = City.getObj(parts[des_index])
        r_str = parts[des_index]
        mls = int(parts[2])
        speed = int(parts[3])
        duration = cls.get_duration(mls, speed)
        highway_count = 1 if speed >= 55 else 0
        hgwy_str = parts[4]
        return cls(des, r_str, mls, duration, hgwy_str, highway_count)

    @classmethod
    def get_duration(self, distance, speed):
        if speed == 0:
            speed = 30
        return float(60 * distance) / speed;

    def __add__(self, other):
        des = other.destination
        r_str = self.route_string + RouteNode.separator + other.route_string
        mls = self.miles + other.miles
        drtn = self.duration + other.duration
        hgwy_str = self.highway_string + RouteNode.separator + other.highway_string
        highway_count = self.highway_count + other.highway_count
        return RouteNode(des, r_str, mls, drtn, hgwy_str, highway_count)

    def __radd__(self, other):
        des = self.destination
        r_str = other.route_string + RouteNode.separator + self.route_string
        mls = other.miles + self.miles
        drtn = other.duration + self.duration
        hgwy_str = other.highway_string + RouteNode.separator + self.highway_string
        highway_count = self.highway_count + other.highway_count
        return RouteNode(des, r_str, mls, drtn, hgwy_str, highway_count)

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

    def human_readable_time(self):
        minutes = self.duration
        if minutes < 60:
            return "%d minutes" % minutes
        hours = minutes / 60
        minutes = hours % 60
        if minutes == 0:
            return "%d Hours" % hours
        return "%d Hours, %d Minutes" % (hours, minutes)

    def __str__(self):
        return self.human_readable_stringify() + "\n" + "%d %s %s" % (
            self.miles, self.format_minutes(), self.route_string.replace('|', ' '))

    def format_minutes(self):
        time = round(float(self.duration) / 60, 4)
        return str(time)

    def human_readable_stringify(self):
        str = "Total Distance: %d miles\n" % (self.miles)
        str += "Time: %s\n" % (self.human_readable_time())
        str += "Start from %s\n" % self.source.name.replace('_',' ')
        places = self.route_string.split(RouteNode.separator)
        highways = self.highway_string.split(RouteNode.separator)

        for i in range(1, len(places)):
            str += "Take %s to reach %s\n" % (highways[i].replace('_', ' '), places[i].replace('_', ' '))
        return str

    def euclidean(self):
        lat1 = self.goal.lat
        lat2 = self.goal.lon
        lon1 = self.destination.lat
        lon2 = self.destination.lon
        square_distance = (lat2 - lat1) ** 2 + (lon2 - lon1) ** 2
        return sqrt(square_distance)

    # Source: http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
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

    # Vincenty distance formula implementation done by the library (source code uploaded along with the submission)
    # Link : https://pypi.python.org/pypi/vincenty/0.1.4
    def vincenty(self):
        lat1 = self.goal.lat
        lat2 = self.goal.lon
        lon1 = self.destination.lat
        lon2 = self.destination.lon
        return vincenty.vincenty((lat1, lon1), (lat2, lon2), True)


class City:
    city_list = {}
    city_data_file = "city-gps.txt"

    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = float(lat)
        self.lon = float(lon)

    @classmethod
    def city_from_file(cls, line):
        parts = line.split()
        if len(parts) == 3:
            return cls(parts[0], parts[1], parts[2])

    @classmethod
    def getObj(cls, city):
        if len(cls.city_list) == 0:
            cls.initialize()
        if city not in cls.city_list:
            cls.city_list[city] = cls(city, 0, 0)
        return cls.city_list[city]

    def __str__(self):
        return self.name

    @classmethod
    def initialize(cls):
        with open(cls.city_data_file) as file:
            for line in file:
                parts = line.split()
                if len(parts) == 3:
                    city_name = parts[0]
                    cls.city_list[city_name] = City(city_name, parts[1], parts[2])
    #Estimate the farthest city
    # @staticmethod
    # def find_farthest_city_from_bloomington():
    #     bloomington_obj = City.getObj("Bloomington,_Indiana")
    #     max_distance_city = ""
    #     max_distance = 0
    #     for obj in City.city_list.values():
    #         if obj.lat ==0 or obj.lon ==0:
    #             continue
    #         distance = City.euclidean(bloomington_obj,obj)
    #
    #         if distance > max_distance:
    #             max_distance = distance
    #             max_distance_city = str(obj)
    #
    #     return max_distance_city
    #
    # @staticmethod
    # def euclidean(from_obj,to_obj):
    #     lat1 = from_obj.lat
    #     lat2 = to_obj.lat
    #     lon1 = from_obj.lon
    #     lon2 = to_obj.lon
    #     square_distance = (lat2 - lat1) ** 2 + (lon2 - lon1) ** 2
    #     return sqrt(square_distance)
