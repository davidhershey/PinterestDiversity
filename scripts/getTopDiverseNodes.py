import argparse
import random
import pickle
import operator
import datetime
from collections import defaultdict
import snap

DATASTRUCTURES_PATH = '../datastructures/'
GRAPH_PATH = '../graphs/'

alpha = .8

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
	global similarityCache
	key = '%s-%s' % (u, x)
	if similarityCache.get(key) is not None:
		return similarityCache[key]
	src = u
	dst = x
	bfsSet = set()
	bfsSet.add(src)
	shortestPath = radius + 1
	for r in range(radius):
		for nodeId in list(bfsSet):
			node = graph.GetNI(nodeId)
			bfsSet = bfsSet.union(list(node.GetOutEdges()))
			# bfsSet = bfsSet.union(list(node.GetInEdges()))
		if dst in bfsSet:
			shortestPath = r + 1
			break
	if shortestPath > radius:
		similarityCache[key] = 0
		return 0
	else:
		result = gamma ** (shortestPath - 1)
		similarityCache[key] = result
		return result 


# Computes the upper bound of diversity of node v, as per the
# Lemma 2 in the MiningDiversity paper
def C(v, radius, gamma, graph):
	neighborhood = rNeighborhood(v, radius, graph)
	cVal = 0
	for neighbor in list(neighborhood):
		cVal += S(neighbor, v, radius, gamma, graph)
	return cVal

def getCList(graph, radius, gamma):
	cList = []
	i = 0.0
	totalNum = graph.GetNodes()
	for node in graph.Nodes():
		nodeId = node.GetId()
		cList.append((nodeId, C(nodeId, radius, gamma, graph)))
		i += 1
		print i / totalNum	
	return cList

def totalS(u, v, radius, gamma, graph):
	uNeighborhood = rNeighborhood(u, radius, graph)
	vNeighborhood = rNeighborhood(v, radius, graph)
	intersect = uNeighborhood.intersection(vNeighborhood)
	total = 0
	for x in list(intersect):
		total += S(v, x, radius, gamma, graph) * S(u, x, radius, gamma, graph)
	return total


def computeUpper(u, v, radius, gamma, graph):
	sPrime = totalS(u, v, radius, gamma, graph)
	summationS = 0
	for x in rNeighborhood(u, radius, graph):
		summationS += S(u, x, radius, gamma, graph)
	if summationS == 0:
		return	
	upper = 1 - alpha * (sPrime / float(summationS))
	return upper

def topkDiverse(graph, cList, radius, gamma, K):
	lowerBound = 0
	T = []
	i = 0
	for tup in cList:
		i += 1
		v = tup[0]
		cv = tup[1]
		if cv < lowerBound:
			return T
		UPv = 0
		vNeighborhood = rNeighborhood(v, radius, graph)
		for u in vNeighborhood:
			upper = computeUpper(u, v, radius, gamma, graph)	
			if not upper:
				continue
			UPv += min(1, upper)
		if UPv < lowerBound:
			continue
		diversity = 0
		for u in vNeighborhood:
			Fuv = computeUpper(u, v, radius, gamma, graph)
			if not Fuv:
				continue
			diversity += Fuv
		if diversity > lowerBound:
			T.append((v, diversity))
		if len(T) > K:
			del T[-1]
			smallestDiversity = sorted(T, key=lambda x:x[1])[0]
			lowerBound = smallestDiversity
		print i / float(len(cList)), diversity
	return T




if __name__ == '__main__':
	global similarityCache
	args = parseArgs()
	similarityCache = {}
	graphName = args.graph
	r = args.r
	gamma = .5
	graph = snap.LoadEdgeList(snap.PNGraph, GRAPH_PATH + graphName + '.txt', 0, 1, '\t')

	# cList = getCList(graph, r, gamma)
	# pickle.dump(cList, open('%s-%s-%s.p' % (DATASTRUCTURES_PATH + graphName, 'cList', r), 'w'))

	cList = pickle.load(open('%s-%s.p' % (DATASTRUCTURES_PATH + graphName, 'cList')))
	cList = sorted(cList, key=lambda x: x[1], reverse=True)
	print cList[:15]
	print topkDiverse(graph, cList, r, gamma, 10)










