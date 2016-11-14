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
fullGraph = snap.TNGraph.New(1100000,5000000)
count = 0
for line in followfile:
    if count%10000 == 0:
        print count
    count+=1
    board_id, follower, created_date = line.split('\t')
    leader,name = board2user[board_id]
    follower = int(follower)
    leader = int(leader)
    if random.random() < .1:
        if not fullGraph.IsNode(follower):
            fullGraph.AddNode(follower)
        if not fullGraph.IsNode(leader):
            fullGraph.AddNode(leader)
        fullGraph.AddEdge(follower,leader)

snap.SaveEdgeList(fullGraph, 'userGraph.txt')
