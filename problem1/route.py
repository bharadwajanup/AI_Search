import problem1.route_algorithms as ra
from problem1.route_segment import routeSegment as rs

origin = "Bloomington,_Indiana"
destination = "Chicago,_Illinois"
#destination = "Indianapolis,_Indiana"
#destination = "Terre_Haute,_Indiana"
#destination = "sfsg" TODO: Handle cases where the city/town does not exist
routing_option="distance"
routing_algorithm="dfs"

def routing_algorithm_implementations(origin_node):
    return {
    "bfs":ra.bfs(origin_node),
    "dfs":ra.dfs(origin_node),
    "ids":print("Use IDS to search"),
    "astar": print("Use astar to search")
}

ra.destination = destination
ra.routing_option = routing_option
ra.source = origin

origin_node = rs(origin,origin,origin,0,0,"")
solution = ra.bfs(origin_node)

if solution:
    print()
    print("Most Optimal Route:")
    solution.machine_readable_stringify()
else:
    print ("Route could not be found")


