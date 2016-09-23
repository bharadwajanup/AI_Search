try:

    from problem1.route_segment import routeSegment as rs
    from problem1.route_segment import City
except Exception:
    from route_segment import routeSegment as rs
    from route_segment import City


segments_data_file = "road-segments.txt"
city_data_file = "city-gps.txt"
segments_dict = {}
segments_cache = {}



def append_to_segments_cache(key,value):
    global segments_cache
    if key not in segments_cache:
        segments_cache[key] = [value]
    else:
        segments_cache[key].append(value)


def initSegmentsCache():
    with open(segments_data_file) as file:
        for line in file:
            parts = line.split()
            if len(parts) == 5:
                if parts[0] not in segments_cache:
                    segments_cache[parts[0]] = [rs.from_file(line,1)]
                else:
                    append_to_segments_cache(parts[0],rs.from_file(line,1))
                if parts[1] not in segments_cache:
                    segments_cache[parts[1]] = [rs.from_file(line,0)]
                else:
                    append_to_segments_cache(parts[1],rs.from_file(line,0))
initSegmentsCache()



def getSegmentsFromDict(destination):
    return segments_cache[destination]

def fetch_segments_new(sourceNode):
    destination_city = sourceNode.destination.name
    road_segments_list = getSegmentsFromDict(destination_city)
    rs_obj_list = []
    for segment in road_segments_list:
        rs_obj_list.append(sourceNode + segment)
    return rs_obj_list


# def getSegmentsFromFile(destination):
#     segments = []
#     with open(segments_data_file) as file:
#         for line in file:
#             parts = line.split()
#             #for now, ignore inconsistent data
#             if len(parts) == 5 and (parts[0] == destination or parts[1] == destination):
#                 segments.append(parts)
#     return segments


# def get_duration(distance, speed):
#     if speed ==0:
#         speed = 30
#     return float(60 * distance)/speed;





# def fetch_segments(sourceNode):
#     destination_city = sourceNode.destination.name
#     road_segments_list = getSegmentsFromFile(destination_city)
#     rs_obj_list = []
#     for segment in road_segments_list:
#         if segment[0] == destination_city:
#             obj_src = segment[0] #deprecated
#             obj_des = getCityObject(segment[1])
#         else:
#             obj_src = segment[1]
#             obj_des = getCityObject(segment[0])
#
#         route_string = sourceNode.route_string+rs.separator+obj_des.name
#         miles = sourceNode.miles + int(segment[2])
#         duration = get_duration(miles,int(segment[3]))
#         highway_string = sourceNode.highway_string+rs.separator+segment[4]
#         rs_obj_list.append(rs(obj_des,route_string,miles,duration,highway_string))
#     return rs_obj_list
#
#
# def getCityInfoFromFile(city_name):
#     with open(city_data_file) as file:
#         for line in file:
#             parts = line.split()
#             if len(parts) == 3:
#                 if parts[0] == city_name:
#                     return parts
#     return None
#
#
# def getCityObject(city_name):
#     city_info = getCityInfoFromFile(city_name)
#     if city_info == None:
#         return City(city_name,0,0)
#     return City(city_info[0],city_info[1],city_info[2])