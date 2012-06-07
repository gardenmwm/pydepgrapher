#!/usr/bin/python
'''
pyDepGrapher

This program creates graphs of from a list of dependencies provided in a csv
file.
It uses graphviz and pydot heavily.

Distributed under MIT licesne

pyDepGrapher Homepage: 	http://code.google.com/p/pydepgrapher/
pydot:			http://code.google.com/p/pydot/
Graphviz		http://www.graphviz.org
@author: gardenmwm
'''
import pydot
import dg

import sys



def makeedge(node1, node2, edgetype, dgconf):
    pe = pydot.Edge( node1, node2 )
    if edgetype in dgconf.EdgeOptions:
        for k, v in dgconf.EdgeOptions[edgetype].iteritems():
            pe.set( k, v )
    return pe

def makenode(nodestring, nodetype, dgconf):
    pn = pydot.Node( nodestring )
    if nodetype in dgconf.NodeOptions:
        for k, v in dgconf.NodeOptions[nodetype].iteritems():
            pn.set( k, v )
    return pn

def makecluster( cluster, nodes, nodelist ):
    pyc = pydot.Cluster( cluster, label = cluster )
    for node in nodes:
        pyc.add_node( nodelist[node] )
    return pyc

def buildgraph( dgconf, deplist ):
    #Build Nodes
    nodelist = {}
    for node in deplist.nodes:
        nodelist[node] = makenode(node, deplist.nodes[node], dgconf)
    #create graph and add nodes
    graph = pydot.Dot( **dgconf.GraphOptions )
    clusters = {}
    #Create subgraphs
    for cluster, nodes in deplist.clusters.iteritems():
         clusters[cluster] = makecluster ( cluster, nodes, nodelist )
    for cluster in clusters:
         graph.add_subgraph( clusters[cluster] )
    for node in nodelist:
        graph.add_node( nodelist[node] )
    #Create Edges
    edgelist = []
    for edge in deplist.edges:
        edgelist.append(makeedge(nodelist[edge[0]], nodelist[edge[1]], edge[2] , dgconf))
    #Add Edges
    for edge in edgelist:
       graph.add_edge( edge )
    #output graph
    graph.write_png( dgconf.GeneralOptions['outfile'] )

if __name__ == "__main__":
   #Setup
   dgconf = dg.depconfig()
   deplist = dg.depstrings( dgconf.GeneralOptions )
   buildgraph( dgconf, deplist )
   print "%d Nodes" % len( deplist.nodes )
   print "%d Dependencies" % len( deplist.edges )
   print "%d Cluster" % len( deplist.clusters )

