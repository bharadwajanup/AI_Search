file_name="myfriends.txt"
table_size = 3
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


print(f_dict)



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

print(solution)