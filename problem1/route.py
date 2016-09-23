"""
(1)Finding the distance between a pair of cities can be formulated as a search problem with states being reaching the
cities, edge weights are the distance between two cities.
Successor function for this problem is reaching the next neighbouring city.
Heuristic function for a*: I used euclidean distance to estimate the distance between a city to the destination.
Euclidean distance only gives the straight line distance and does not overestimate. Hence, it can be admissable.

(2) Four search algorithms have been implemented for this problem

1. BFS: It is a blind searching technique which simply looks for the destination city by traversing every neighbour
of a city. The branching factor is high as it traverses breadth-wise in the tree. The algorithm, although slow,
is complete.
2. DFS: Another blind searching strategy which looks for the goal state by branching deep into the child nodes
of the tree. It can go to infinite loops when there are cycles and is not considered complete.
3. IDS: An improvisation of DFS which searches the tree where the level of the tree is increased at each iteration
 and DFS is applied. Significantly faster than BFS and could be a preferred blind search strategy for these
 kind of problems.
4. A*: A* is a search algorithm which makes use of a heuristic function to reach the goal state. The cost function
can be defined as
                                                f = g+h
where g is the distance travelled to the node and h is the estimated distance to the destination.

(3) The code:
The program looks for its neighbouring cities, updates the distance, route and other parameters, adds it as
a successor and keeps going until a goal state is achieved. A goal state is simply a route from the source to the
destination. However, the state space becomes too large if the code keeps branching out to find the goal.
To reduce the state space, it is ensured that there are no cycles (don't consider a neighbouring city who is
either a source or one of the cities visited during the route) and the route to any intermediate city is always the
most optimal one based on the routing option desired. There could be many routes to reach a city. To ensure we
get the most optimal route, we keep comparing with every other state after one of the branches reach the destination
to see if there are better routes. Thus, at the end, we are only left with the optimal route to the destination.

The road segments and the city co-ordinates are loaded into a dictionary for faster access.

For ids, we optimize it by ensuring that at each level, we only find successors for the nodes who have reached
till the previous level avoiding redundant states.

Class RouteNode holds all the information that helps in tracing the route and calculate parameters to aid
the routing options

Class City holds the co-ordinates of a city.

Assumptions and simplifications:
The program does not consider the lines in road-segments.txt that has incomplete information
Any road segment without a speed information will be set to a default value 30 for simplicity.
If there is a highway instead of a city name as the node, it is treated as a neighbouring city but is not
honoured with an estimated co-ordinate values. Instead a default value of (0,0) is assigned. This does come in
the way of a* search and might disrupt the route, but the extra cost is minimum for this program and it always
gets back to the optimal route eventually. This is one of the things that could have been handled better.

"""
"""
Analysis:
(1) Which search algorithm seems to work best for each
routing options?
Ans:
distance: a* since the heuristic function was on estimated distance to the destination.
segments: ids as it only needs to go to a certain depth to find the goal state.
time: a* performed better with this implementation
scenic: ids performed better with this implementation

(2) Which algorithm is fastest in terms of the amount of computation time required
by your program, and by how much, according to your experiments?
Ans:
When it comes to distance routing option, a* was the fastest to find the route to the destination. While the
difference was not so much for shorter distances, a* was at least twice as fast for long distances. Below is
a sample system execution times all of algorithms
Source: Bloomington,_Indiana
Destination: Seattle, Washington
routing-option: distance

Execution time:
ids: 0.203s
astar: 0.078s
bfs: 0.125s
dfs: took too long

(3) Which algorithm requires the least memory, and by how much, according to your
experiments?
Ans:
a* search requires the least amount of memory and has the potential to further reduce it with a better
heuristic function.
The following is a sample result of the number of successor elements each algorithm had at the end of its execution:
Source: Bloomington,_Indiana
Destination: Seattle, Washington
routing-option: distance

bfs: 261838 elements
ids: 67686 elements
a*: 8094 elements

(4) Which heuristic function did you use, how good is it, and how might you make it
better?
Ans:
I used euclidean distance to estimate the distance to the destination. I also tried haversine and vincent estimations
which takes into account the spherical nature of the earth. However, I did not see any substantial difference in
the performance in the algorithm.
One way the heuristics could be made better is to use a combination of euclidean distance and routing option specific
heuristics thereby we traverse through a branch which is both closer to the destination and also satisfies the
routing option requirements. I could think of some things like calculate the mean speed limit of US roads and
use it as a basis for estimating time required to reach the destination, calculate the number of highways in each state,
the number of states you need to pass to reach the goal and estimate the number of segments you might need to reach
the destination.

(5) Supposing you start in Bloomington, which city should you travel to if you want to take
the longest possible drive (in miles) that is still the shortest path to that city? (In other words, which
city is furthest from Bloomington?)
Ans:
The farthest city from Bloomington is Skagway, Alaska with a distance of 4542 miles from Bloomington.
"""

import sys

try:
    import problem1.route_algorithms as ra
    from problem1.route_segment import RouteNode
    from problem1.route_segment import City
except ImportError:
    import route_algorithms as ra
    from route_segment import RouteNode
    from route_segment import City

if len(sys.argv) != 5:
    print("Invalid Command Line Parameters:")
    print("python route.py [start-city] [end-city] [routing-option] [routing-algorithm]")
    exit(1)

origin = sys.argv[1]
destination = sys.argv[2]
routing_option = sys.argv[3]
routing_algorithm = sys.argv[4]


def routing_algorithm_implementations(algorithm, origin_node):
    if algorithm == "bfs":
        return ra.bfs(origin_node)
    elif algorithm == "dfs":
        return ra.dfs(origin_node)
    elif algorithm == "ids":
        return ra.ids_optim(origin_node)
    elif algorithm == "astar":
        return ra.a_star(origin_node)
    else:
        print("Unknown Algorithm")


ra.destination = destination
ra.routing_option = routing_option
ra.source = origin

RouteNode.source = City.getObj(origin)
RouteNode.goal = City.getObj(destination)
if RouteNode.source.lat == 0 or RouteNode.goal.lat == 0:
    print("Invalid source or destination")
    exit(1)
origin_node = RouteNode(RouteNode.source, origin, 0, 0, "", 0)
solution = routing_algorithm_implementations(routing_algorithm, origin_node)

if solution:
    print("\n")
    print("Optimal Route:")
    print(solution)
    print("\n\n")
    # print("Fringe had %d elements" % ra.fringe_counter)
    # farthest_city = City.find_farthest_city_from_bloomington()
    # print("Estimated farthest city is %s" % farthest_city)
else:
    print("Route could not be found")
