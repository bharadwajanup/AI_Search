import problem1.fetch_route_data as rd
destination=""
routing_option = ""
source = ""
goal_state = None

def matches_option(cur_node, prev_node):
    return {'segments': len(cur_node.route_string.split(',')) < len(prev_node.route_string.split(',')),
            'distance': cur_node.miles < prev_node.miles, 'time': cur_node.duration < prev_node.duration,
            'scenic': False}

def is_best_route(node_segment):
    destination_city = node_segment.destination
    if destination_city == source or destination_city in node_segment.route_string.rpartition(',')[0]:
        return False
    if goal_state != None and matches_option(goal_state,node_segment).get(routing_option,False):
        return False

    if destination_city not in rd.segments_dict or matches_option(node_segment,rd.segments_dict[destination_city]).get(routing_option,False):
        rd.segments_dict[destination_city] = node_segment
        return True
    return False



def successors(node_segment):
    child_objects = rd.fetch_segments(node_segment)
    successors_list = []
    for rs_obj in child_objects:
        if is_best_route(rs_obj):
            successors_list.append(rs_obj)
    return successors_list



def is_goal(obj):
    return obj.destination == destination


def bfs(origin_node):
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

def dfs(origin_node):
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
            fringe.append(s)
    if goal_state == None:
        return False
    print("Routes Found")
    for route in all_goal_states:
        route.machine_readable_stringify()
    return goal_state