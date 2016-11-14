import snap


graph = snap.LoadEdgeList(snap.PNGraph, 'firstMillionGraph.txt', 0, 1)

snap.DrawGViz(graph, snap.gvlDot, "graph.png", "graph 1")
