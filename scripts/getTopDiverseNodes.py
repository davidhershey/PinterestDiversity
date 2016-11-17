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
	parser.add_argument('--r', help='radius r (1-4) parameter for calculating diversity', default=2, type=int)
	args = parser.parse_args()
	return args	


# Creates the small neighborhood of nodes that are
# within radius of node v
# RETURNS: the set of nodeIds that make up the neighborhood
# NOTE: We are assuming out-edges as edges to neighbors
def rNeighborhood(v, radius, graph):
	neighborhood = set()
	neighborhood.add(v)
	for r in range(radius):
		for nodeId in list(neighborhood):
			node = graph.GetNI(nodeId)
			neighborhood = neighborhood.union(list(node.GetOutEdges()))
	neighborhood.remove(v)
	return neighborhood


# Calculates the similarity from node u and x, as defined by 
# Definition 3 in the MiningDiversity paper
# Basically, if the path between them is > radius, then its 0;
# otherwise it is gamma ^ (shortestpath - 1)
# RETURNS: similarity metric
# NOTE: We take both in and out edges into account for this distance
def S(u, x, radius, gamma, graph):
	src = u
	dst = x
	bfsSet = set()
	bfsSet.add(src)
	shortestPath = radius + 1
	for r in range(radius):
		for nodeId in list(bfsSet):
			node = graph.GetNI(nodeId)
			bfsSet = bfsSet.union(list(node.GetOutEdges()))
			bfsSet = bfsSet.union(list(node.GetInEdges()))
		if dst in bfsSet:
			shortestPath = r + 1
			break
	if shortestPath > radius:
		return 0
	else:
		return gamma ** (shortestPath - 1)


# Computes the upper bound of diversity of node v, as per the
# Lemma 2 in the MiningDiversity paper
def C(v, radius, gamma, graph):
	neighborhood = rNeighborhood(v, radius, graph)
	cVal = 0
	for neighbor in list(neighborhood):
		cVal += S(neighbor, v, radius, gamma, graph)
	return cVal

def getSortedCList(graph, radius, gamma):
	cList = []
	i = 0.0
	totalNum = graph.GetNodes()
	for node in graph.Nodes():
		nodeId = node.GetId()
		cList.append((nodeId, C(nodeId, radius, gamma, graph)))
		i += 1
		print i / totalNum	
	return cList

if __name__ == '__main__':
	args = parseArgs()
	graphName = args.graph
	r = args.r
	gamma = .5
	graph = snap.LoadEdgeList(snap.PNGraph, GRAPH_PATH + graphName + '.txt', 0, 1, '\t')

	v = graph.GetNI(1)
	# print (list(v.GetOutEdges()))

	cList = getSortedCList(graph, r, gamma)
	pickle.dump(cList, open('%s-%s.p' % (DATASTRUCTURES_PATH + graphName, 'cList'), 'w'))
