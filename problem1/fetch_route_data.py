try:

    from problem1.route_segment import RouteNode
    from problem1.route_segment import City
except ImportError:
    from route_segment import RouteNode
    from route_segment import City

segments_data_file = "road-segments.txt"
city_data_file = "city-gps.txt"
segments_dict = {}
segments_cache = {}


def append_to_segments_cache(key, value):
    global segments_cache
    if key not in segments_cache:
        segments_cache[key] = [value]
    else:
        segments_cache[key].append(value)


def init_segments_cache():
    with open(segments_data_file) as file:
        for line in file:
            parts = line.split()
            if len(parts) == 5:
                if parts[0] not in segments_cache:
                    segments_cache[parts[0]] = [RouteNode.from_file(line, 1)]
                else:
                    append_to_segments_cache(parts[0], RouteNode.from_file(line, 1))
                if parts[1] not in segments_cache:
                    segments_cache[parts[1]] = [RouteNode.from_file(line, 0)]
                else:
                    append_to_segments_cache(parts[1], RouteNode.from_file(line, 0))


init_segments_cache()


def get_segments_from_dict(destination):
    return segments_cache[destination]


def fetch_segments_new(sourceNode):
    destination_city = sourceNode.destination.name
    road_segments_list = get_segments_from_dict(destination_city)
    rs_obj_list = []
    for segment in road_segments_list:
        rs_obj_list.append(sourceNode + segment)
    return rs_obj_list
