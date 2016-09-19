from problem1.route_segment import routeSegment as rs
segments_data_file = "road-segments.txt"
segments_dict = {}

def getSegmentsFromFile(destination):
    segments = []
    with open(segments_data_file) as file:
        for line in file:
            parts = line.split()
            #for now, ignore inconsistent data
            if len(parts) == 5 and (parts[0] == destination or parts[1] == destination):
                segments.append(parts)
    return segments


def get_duration(distance, speed):
    if speed ==0:
        speed = 30
    return float(60 * distance)/speed;


def fetch_segments(sourceNode):
    destination_city = sourceNode.destination
    road_segments_list = getSegmentsFromFile(destination_city)
    rs_obj_list = []
    for segment in road_segments_list:
        if segment[0] == destination_city:
            obj_src = segment[0] #deprecated
            obj_des = segment[1]
        else:
            obj_src = segment[1]
            obj_des = segment[0]

        route_string = sourceNode.route_string+rs.separator+obj_des
        miles = sourceNode.miles + int(segment[2])
        duration = get_duration(miles,int(segment[3]))
        highway_string = sourceNode.highway_string+rs.separator+segment[4]
        rs_obj_list.append(rs(obj_des,route_string,miles,duration,highway_string))
    return rs_obj_list


