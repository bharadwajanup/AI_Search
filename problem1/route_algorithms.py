try:
    import problem1.fetch_route_data as rd
    from problem1.route_segment import routeSegment as rs
    import queue as Queue
except Exception:
    import fetch_route_data as rd
    from route_segment import routeSegment as rs
    import Queue
destination=""
routing_option = ""
source = ""
goal_state = None
max_depth_level = 2000 #arbitrary max levels to return from the loop for IDS
def matches_option(cur_node, prev_node):
    return {'segments': cur_node.level < prev_node.level,
            'distance': cur_node.miles < prev_node.miles,
            'time': cur_node.duration < prev_node.duration,
            'scenic': False}#TODO: Work on Scenic

def is_best_route(node_segment):
    destination_city = node_segment.destination.name
    if destination_city == source or destination_city in node_segment.route_string.rpartition(rs.separator)[0]:
        return False
    if goal_state != None and matches_option(goal_state,node_segment).get(routing_option,False):
        return False

    if destination_city not in rd.segments_dict or matches_option(node_segment,rd.segments_dict[destination_city]).get(routing_option,False):
        rd.segments_dict[destination_city] = node_segment
        return True
    return False



def successors(node_segment,level=None):
    successors_list = []
    if level != None and node_segment.level == level:
        return successors_list
    child_objects = rd.fetch_segments(node_segment)

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
    all_goal_states =[]
    while len(fringe)>0:
        for s in successors(fringe.pop()):
            if is_goal(s):
                all_goal_states.append(s)
                if goal_state == None or matches_option(s,goal_state).get(routing_option,False):
                    goal_state = s
                #return s
            fringe.insert(0,s)
    if goal_state == None:
        return False
    print("Routes Found")
    for route in all_goal_states:
        route.machine_readable_stringify()
    return goal_state

def dfs(origin_node,level=None):
    fringe = [origin_node]
    global goal_state
    #all_goal_states =[]
    while len(fringe)>0:
        for s in successors(fringe.pop(),level):
            if is_goal(s):
                print("Route Found")
                s.machine_readable_stringify()
                if goal_state == None or matches_option(s,goal_state).get(routing_option,False):
                    goal_state = s
            fringe.append(s)
    if goal_state == None:
        return False
    return goal_state

def ids(origin_node):
    depth = 0
    while depth < max_depth_level:
        print("Depth: %d" %depth)
        rd.segments_dict.clear() #Clear the dictionary as we are performing a new search every iteration
        solution = dfs(origin_node,depth)
        #if solution:
         #   return solution
        depth = depth+1
    return solution

def ids_optim(origin_node):
    if origin_node.destination.name == destination:
        return origin_node
    depth = 1

    while True:
        print("Depth: %d" %depth)
        if depth == 1:
            solution = dfs(origin_node,depth)
            depth+=1
            continue
        #Instead of recalculating from the beginning every time, make use of the pre-calculated values and search from that point.
        depth_origins = [obj for obj in rd.segments_dict.values() if obj.level == depth -1]

        if len(depth_origins) == 0:
            break
        for origin_obj in depth_origins:
            solution = dfs(origin_obj,depth)
        #if solution:
         #   return solution
        depth = depth+1
    return solution

def hieuristic(nodeSegment):
    return float(nodeSegment.miles + nodeSegment.est_distance)

#TODO: Astar: For calculating the straight line distance, we can make use of the co-ordinates given in the city-gps.txt
def astar(origin_node):
    fringe = Queue.PriorityQueue()
    fringe.put((hieuristic(origin_node),origin_node))
    global goal_state
    while not fringe.empty():
        for s in successors(fringe.get()[1]):
            if is_goal(s):
                print("Route Found")
                s.machine_readable_stringify()
                if goal_state == None or matches_option(s, goal_state).get(routing_option, False):
                    goal_state = s
            try:
                fringe.put((hieuristic(s),s))
            except Exception:
                #print("There was an exception at %s" %s.machine_readable_stringify())
                print("There was an exception thrown")
    if goal_state == None:
        return False
    return goal_state

