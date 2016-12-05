import snap
import random
import pickle
import operator
import datetime
from collections import defaultdict

print 'Loading Boards'
boardfile = open('../data/boards.tsv')
board2user  = {}
user2boards = []
for line in boardfile:
    board_id, board_name, board_description, user_id, board_create_time = line.split('\t')
    board2user[board_id] = (user_id,board_name)
    user2boards.append((board_id,board_name))
boardfile.close()
print 'Loaded Boards'
print 'Loading Follows'
edgesDates = []
followfile = open('../data/follow.tsv')
count = 0
for line in followfile:
    if count%100000==0:
        print count
    count+=1
    board_id, follower, created_date = line.split('\t')
    date = datetime.datetime.strptime(created_date, '%Y-%m-%d\n')
    leader,name = board2user[board_id]
    if follower == leader:
        continue #eliminate self loops
    edgesDates.append((follower,leader,date))

print 'Loaded Follows'

print 'Sorting'
sorted_by_date = sorted(edgesDates, key=lambda tup: tup[2])
print 'Writing'


outfile = open('../graphs/fullEdgesByDate.txt','w')
for i in range(len(sorted_by_date)):
    src,dst,date = sorted_by_date[i]
    outfile.write('{}\t{}\t{}\n'.format(src,dst,date))

# pickle.dump(sorted_by_date,open('EdgesByDate.p','w'))
outfile.close()
# top_degs = pickle.load(open('top_degs.p'))
# top_deg = open('top_deg.txt','w')
# for user,deg in top_degs:
#     top_deg.write("{}\t{}\n".format(user,deg))
