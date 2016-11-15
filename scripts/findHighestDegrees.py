import snap
import random
import pickle
import operator
from collections import defaultdict
# userfile = open('../data/users.tsv')
numToSample = 100000
# users = []
# for line in userfile:
#     users.append(int(line))
# userfile.close()

boardfile = open('../data/boards.tsv')
board2user  = {}
user2boards = []
for line in boardfile:
    board_id, board_name, board_description, user_id, board_create_time = line.split('\t')
    board2user[board_id] = (user_id,board_name)
    user2boards.append((board_id,board_name))
boardfile.close()
print 'Loaded Boards'

follows = {}
followfile = open('../data/follow.tsv')
indegs = defaultdict(int)
for line in followfile:
    board_id, follower, created_date = line.split('\t')
    leader,name = board2user[board_id]
    indegs[leader] +=1

print 'Loaded Follows'

print 'Sorting'
sorted_by_indeg = sorted(indegs.items(), key=operator.itemgetter(1),reverse=True)
pickle.dump(sorted_by_indeg,open('top_degs.p','w'))

# top_degs = pickle.load(open('top_degs.p'))
# top_deg = open('top_deg.txt','w')
# for user,deg in top_degs:
#     top_deg.write("{}\t{}\n".format(user,deg))
