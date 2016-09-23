import sys
try:
    import problem1.route_algorithms as ra
    from problem1.route_segment import routeSegment as rs
    from problem1.route_segment import City as City
except Exception:
    import route_algorithms as ra
    from route_segment import routeSegment as rs
from problem1.route_segment import City as City



if len(sys.argv) != 5:
    print("Invalid Command Line Parameters:")
    print("python route.py [start-city] [end-city] [routing-option] [routing-algorithm]")
    exit(1)
origin = sys.argv[1]
destination = sys.argv[2]
routing_option= sys.argv[3]
routing_algorithm = sys.argv[4]
# origin = "Bloomington,_Indiana"
# #destination = "Chicago,_Illinois"
# #destination = "Indianapolis,_Indiana"
# #destination = "Cincinnati,_Ohio"
# destination = "Pittsburgh,_Pennsylvania"
# #destination = "Seattle,_Washington"
# #destination = "sfsg"
# routing_option="scenic"
# routing_algorithm="astar"



def routing_algorithm_implementations(algorithm,origin_node):
    if algorithm == "bfs":
        return ra.bfs(origin_node)
    elif algorithm == "dfs":
        return ra.dfs(origin_node)
    elif algorithm == "ids":
        return ra.ids_optim(origin_node)
    elif algorithm == "astar":
        return ra.astar(origin_node)
    else:
        print("Unknown Algorithm")


ra.destination = destination
ra.routing_option = routing_option
ra.source = origin

rs.source = City.getObj(origin)
rs.goal = City.getObj(destination)
if rs.source.lat == 0 or rs.goal.lat == 0:
    print("Invalid source or destination")
    exit(1)
origin_node = rs(rs.source,origin,0,0,"",0)
solution = routing_algorithm_implementations(routing_algorithm,origin_node)

if solution:
    print("\n")
    print("Most Optimal Route:")
    print(solution)
else:
    print ("Route could not be found")


