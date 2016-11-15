
from collections import defaultdict
import snap
graph = snap.LoadEdgeList(snap.PNGraph, '../graphs/first50kGraph.txt', 0, 1)

print 'Loading Boards'
boardfile = open('../data/boards.tsv')
board2user  = {}
user2boards = defaultdict(list)
for line in boardfile:
    board_id, board_name, board_description, user_id, board_create_time = line.split('\t')
    board2user[board_id] = (user_id,board_name)
    user2boards[int(user_id)].append((board_id,board_name))


input = raw_input('Enter UId: ')
while input != '':
    if int(input) in user2boards:
        n = graph.GetNI(int(input))
        print n.GetInDeg(),n.GetOutDeg()
        print user2boards[int(input)]

    else:
        print "User not found"
    input = raw_input('Enter UId: ')
