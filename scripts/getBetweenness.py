import argparse
import random
import pickle
import operator
import datetime
from collections import defaultdict
import snap

DATASTRUCTURES_PATH = '../datastructures/'
GRAPH_PATH = '../graphs/'

def parseArgs():
	parser = argparse.ArgumentParser(description='Calculate Betweenness')
	parser.add_argument('--graph', help='Name of graph file in edge list form to load', required=True)
	args = parser.parse_args()
	return args.graph

def getTopBetweennessNodes(nodeBetweennessDict, numNodes):
	result = []
	ite = nodeBetweennessDict.BegI()
	for i in range(numNodes):
		nodeId = int(ite.GetKey())
		bCentrality = ite.GetDat() 
		result.append((nodeId, bCentrality))
		ite.Next()
	return result

if __name__ == '__main__':
	graphName = parseArgs()
	graph = snap.LoadEdgeList(snap.PNGraph, GRAPH_PATH + graphName + '.txt', 0, 1, '\t')

	dataFilename = DATASTRUCTURES_PATH + graphName + '_betweenness_hash'

	betweennessDict = snap.TIntFltH()
	edgeBetweennessDict = snap.TIntPrFltH()
	snap.GetBetweennessCentr(graph, betweennessDict, edgeBetweennessDict, .75, True)
	betweennessNodeFOut = snap.TFOut(dataFilename)
	betweennessDict.Save(betweennessNodeFOut)

	# betweennessNodeFIn = snap.TFIn(dataFilename)
	# betweennessDict = snap.TIntFltH()
	# betweennessDict.Load(betweennessNodeFIn)
	# betweennessDict.SortByDat(False)

	topBetweennessNodes = getTopBetweennessNodes(betweennessDict, 20)

	

	
