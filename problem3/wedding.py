# Assignment 1 - Question 3

# I think it is simple.
# Given the number of seats per table, it fills up the people at the table but the people in the same row cannot be sitted at the same table just like the queens problem.
# The difference is that each name should be used once.
# Moreover, every name should be used.
# So, by putting the list of friends into the table, count the number of lines and the number of columns in each line.
#

data = 'myfriends.txt'
file = open(data, 'r')
lines = file.readlines()

print 'read', len(lines), 'lines from', data

# Number of rows in each line
row = 0
for i in range(0,len(lines)):
    # I am not sure how to distinguish rows... How should i code to divide rows when the text is given with "space"
    # So for i in range(0, len(lines)), if there is a space, it counts one and it should count for each line.
    if
    return count( [lines[col] for lines in data] )

print(len(lines))
print()

# Once it is done counting, I believe I should give it positions for each name so that they  can be separated from the relationships.
# I am thinking about placing the first name (0,0) in the first place then let the program search for the name that is not used and not in the same line.
#def function(name,line):
# Various search functions can be applied just like n-queen problem. However, I believe it can be solved quite quickly by giving constraints that each name should be used once,
# Only one name can be used for the same table in the same line, the number of people in the same table will be limited as well so when the table is filled without picking the names from the same line, it will move to the next table to fill up again. Then, it should have the least number of talbes.
# Heuristic function for this one is by counting the number of lines, which will be the least number of tables.
# Another possibility is that number of people in one line, which will also be the least number of tables needed.
# Even if those two are combinbed, I think it is admissible.