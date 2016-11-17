import snap
from collections import defaultdict

# print 'Loading Boards'
# boardfile = open('../data/boards.tsv')
# board2user  = {}
# user2boards = defaultdict(list)
# for line in boardfile:
#     board_id, board_name, board_description, user_id, board_create_time = line.split('\t')
#     board2user[board_id] = (user_id,board_name)
#     user2boards[int(user_id)].append((board_id,board_name))


graph = snap.LoadEdgeList(snap.PNGraph, '../graphs/firstMillionGraph.txt', 0, 1)

degs = []

for n in graph.Nodes():
    degs.append((n.GetId(),min([n.GetInDeg(),n.GetOutDeg()])))

degs.sort(key=lambda tup: tup[1],reverse=True)

for i in range(20):
    nid = degs[i][0]
    n = graph.GetNI(nid)
    print "Node: {}\tInDeg: {}\tOutDeg: {}".format(nid,n.GetInDeg(),n.GetOutDeg())
