import sys

import problem1.route_algorithms as ra
from problem1.route_segment import routeSegment as rs

origin = "Bloomington,_Indiana"
destination = "Chicago,_Illinois"
#destination = "Indianapolis,_Indiana"
#destination = "Cincinnati,_Ohio"
destination = "Pittsburgh,_Pennsylvania"
#destination = "sfsg" TODO: Handle cases where the city/town does not exist
routing_option="distance"
routing_algorithm="ids"

def routing_algorithm_implementations(algorithm,origin_node):
    if algorithm == "bfs":
        return ra.bfs(origin_node)
    elif algorithm == "dfs":
        return ra.dfs(origin_node)
    elif algorithm == "ids":
        return ra.ids_optim(origin_node)
    elif algorithm == "astar":
        print("A star search")
        return False
    else:
        print("Unknown Algorithm")


ra.destination = destination
ra.routing_option = routing_option
ra.source = origin

rs.source = origin
origin_node = rs(origin,origin,0,0,"")
solution = routing_algorithm_implementations(routing_algorithm,origin_node)

if solution:
    print()
    print("Most Optimal Route:")
    solution.machine_readable_stringify()
else:
    print ("Route could not be found")


