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

print "This Graph has ",graph.GetNodes(), " nodes"
print "This Graph has ",graph.GetEdges(), " edges"

snap.PrintInfo(graph, "Python type PNEANet")

n = graph.GetNI(snap.GetMxInDegNId(graph))

print 'Max in degree node:', n.GetId()
print 'In degree: ',n.GetInDeg()
print 'Out degree:',n.GetOutDeg()

# print user2boards[int(n.GetId())
print 'Calculating Page Rank'
PRankH = snap.TIntFltH()
snap.GetPageRank(graph, PRankH)

betw = []
for n in PRankH:
    betw.append((n,PRankH[n]))

betw_s = sorted(betw, key=lambda tup: tup[1],reverse=True)
for i in range(20):
    print i+1,". ",betw_s[i][0],betw_s[i][1]
