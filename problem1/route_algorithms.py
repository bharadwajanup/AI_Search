try:
    import problem1.fetch_route_data as rd
    from problem1.route_segment import RouteNode
    import queue as Queue
except ImportError:
    import fetch_route_data as rd
    from route_segment import RouteNode
    import Queue

destination = ""
routing_option = ""
source = ""
goal_state = None

# arbitrary max levels to return from the loop for IDS
max_depth_level = 2000


def matches_option(cur_node, prev_node):
    return {'segments': cur_node.level < prev_node.level,
            'distance': cur_node.miles < prev_node.miles,
            'time': cur_node.duration < prev_node.duration,
            'scenic': cur_node.highway_count < prev_node.highway_count}


def is_best_route(node_segment):
    destination_city = node_segment.destination.name
    if destination_city == source or destination_city in node_segment.route_string.rpartition(RouteNode.separator)[0]:
        return False
    if goal_state is not None and matches_option(goal_state, node_segment).get(routing_option, False):
        return False

    if destination_city not in rd.segments_dict or matches_option(node_segment, rd.segments_dict[destination_city]).get(
            routing_option, False):
        rd.segments_dict[destination_city] = node_segment
        return True
    return False


def successors(node_segment, level=None):
    successors_list = []
    if level is not None and node_segment.level == level:
        return successors_list
    child_objects = rd.fetch_segments_new(node_segment)

    for rs_obj in child_objects:
        if is_best_route(rs_obj):
            successors_list.append(rs_obj)
    return successors_list


def is_goal(obj):
    return obj.destination.name == destination


def bfs(origin_node):
    print("BFS")
    fringe = [origin_node]
    global goal_state
    while len(fringe) > 0:
        for s in successors(fringe.pop()):
            if is_goal(s):
                if goal_state is None or matches_option(s, goal_state).get(routing_option, False):
                    goal_state = s
                    # return s
            fringe.insert(0, s)
    if goal_state is None:
        return False
    return goal_state


def dfs(origin_node, level=None):
    fringe = [origin_node]
    global goal_state
    while len(fringe) > 0:
        for s in successors(fringe.pop(), level):
            if is_goal(s):
                if goal_state is None or matches_option(s, goal_state).get(routing_option, False):
                    goal_state = s
            fringe.append(s)
    if goal_state is None:
        return False
    return goal_state


def ids(origin_node):
    depth = 0
    while depth < max_depth_level:
        print("Depth: %d" % depth)
        rd.segments_dict.clear()  # Clear the dictionary as we are performing a new search every iteration
        solution = dfs(origin_node, depth)
        depth += 1
    return solution


def ids_optim(origin_node):
    if origin_node.destination.name == destination:
        return origin_node
    depth = 1

    while True:
        print("Depth: %d" % depth)
        if depth == 1:
            solution = dfs(origin_node, depth)
            depth += 1
            continue
        # Instead of recalculating from the beginning every time, make use of the pre-calculated values
        # and search from that point.
        depth_origins = [obj for obj in rd.segments_dict.values() if obj.level == depth - 1]

        if len(depth_origins) == 0:
            break
        for origin_obj in depth_origins:
            solution = dfs(origin_obj, depth)
        depth += 1
    return solution


def heuristics(node_segment):
    return float(node_segment.miles + node_segment.euclidean())


def a_star(origin_node):
    fringe = Queue.PriorityQueue()
    fringe.put((heuristics(origin_node), origin_node))
    global goal_state
    while not fringe.empty():
        for s in successors(fringe.get()[1]):
            if is_goal(s):
                print("Route Found")
                if goal_state == None or matches_option(s, goal_state).get(routing_option, False):
                    goal_state = s
            fringe.put((heuristics(s), s))
    if goal_state is None:
        return False
    return goal_state
