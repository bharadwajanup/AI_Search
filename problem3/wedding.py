# Assignment 1 - Question 3
import sys
#print sys.argv

#   For each problem, please write a detailed comments section at the top of your code that includes: (1) a description of how you formulated the search problem, including precisely defining the state space, the successor function, the edge weights, and (if applicable) the heuristic function(s) you designed, including an argument for why they are admissible; (2) a brief description of how your search algorithm works; (3) and discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made.

# For Question 3, the friends list was recorded in the dictionary with each first person in the line as key and the person's friends as values. Then, each person was assigned to the table with the relationship kept in mind. The way  of assigning was simple. The list begins with everybody not seated, then a person is assigned to a table. Then, when the next person is assigned, it was checked to see if they are friends, if they are not friends, they are sit together, but if they are friends, the second person is assigned to a new table. Then, for the thrid person, the same procedure is applied. Once all seats are assigned for a table, it was excluded from assigning. Moreover, once the person is assigned, the person was removed from the list so that everybody is assigned without missing anybody.

# The state space is all the possible assignment of the people from the source text file to the number of seats per table given from the commandline.  In the search function or start_assigning, Initial state in this case would be the assign list, which is empty since nobody is assigned in the beginning and the final goal state would be everybody assigned with no friends in the same table. Successor function would be either assigning the person in the exisiting table or in the new table depending on the relationship. Moreover, the cost function would be the number of people in the list since each step will take one person from the list until the list becomes empty. Lastly, the edge weight is the number of relations that needs to be searched or checked in order to reach the successor node.

# There were few problems at the beginning of the project. In the beginning, I thought it was much simpler problem just like rook problems. I thought it was simply putting the person in the same line of the list not to be assigned together, so creating a table from the list was considered in the beginning, which was not the case. Realizing it to be more complicated than that, we had to come up with some other ideas such as dictionaries. Graph coloring was also considered to be an option in the discussion as well. Moreover, making sure everybody is assigned was another issue since same name could appear more than once in the list, so creating a name list with 0 before assigned and 1 after assigned was considered in the beginning of the discussion. However, a better way of putting this was found, which was popping out the person assigned from the list and the list to be empty at the end of the assignment.

file_name = sys.argv[1]
table_size = int(sys.argv[2])
f_dict = {}

def createFriendsDict():
    dict={}
    with open(file_name) as file:
        for line in file:
            list_of_friends = line.split()
            if len(list_of_friends)==0:
                continue
            person = list_of_friends.pop(0)
            if person not in dict:
                dict[person] = list_of_friends
            else:
                dict[person]+=list_of_friends
            for friend in list_of_friends:
                if friend not in dict:
                    dict[friend] = [person]
                else:
                    dict[friend].append(person)
    return dict

f_dict = createFriendsDict()

def start_assigning():
    global f_dict
    assign_list = []
    for person in f_dict.keys():
        is_seated = False
        for table in assign_list:
            can_be_seated = True
            if len(table) < table_size:
                for seated_person in table:
                    if f_dict[seated_person].count(person) > 0:
                        can_be_seated = False
                        break
                if can_be_seated:
                    table.append(person)
                    is_seated = True
                    break
            is_seated = False
        if not is_seated:
            assign_list.append([person])
    return assign_list

solution = start_assigning()

print len(solution), solution
