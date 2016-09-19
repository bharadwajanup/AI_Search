
class routeSegment:
    'Object for holding the route between two nodes'
    separator = '|'
    source = ""
    def __init__(self,destination,route_string,miles,duration,highway_string):
        #self.source = source
        self.destination = destination
        self.route_string = route_string
        self.miles = miles
        self.duration = duration #in minutes
        self.highway_string = highway_string
        self.level = len(self.route_string.split(self.separator)) - 1

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

