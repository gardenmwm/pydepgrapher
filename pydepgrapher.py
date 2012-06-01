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



def makeedge(node1,node2,edgetype):
    pe=pydot.Edge(node1,node2)
    if edgetype in EdgeOptions:
        for k,v in EdgeOptions[edgetype].iteritems():
            pe.set(k,v)
    return pe

def makenode(nodestring,nodetype):
    pn=pydot.Node(nodestring)
    if nodetype in NodeOptions:
        for k,v in NodeOptions[nodetype].iteritems():
            pn.set(k, v)
    return pn





if __name__=="__main__":
   
   #Build Nodes
   dg.depconfig()
   nodelist={}
   for node in nodestrings:
       nodelist[node]=makenode(node,nodestrings[node])
   
   #create graph and add nodes
   graph=pydot.Dot(**GraphOptions)
   clusters={}
   #Create subgraphs
   for cluster, nodes in clusterstrings.iteritems():
        clusters[cluster]=pydot.Cluster(cluster,label=cluster)
        print nodes
        for node in nodes:
            clusters[cluster].add_node(nodelist[node])
            #del(nodelist[node]) #Don't want to add it twice
        
   #graph=pydot.Dot(graph_type='digraph',ratio=1.3,layout='dot',sep='+1',overlap='scalexy')
   print "Adding Nodes"
   for cluster in clusters:
        graph.add_subgraph(clusters[cluster])
   for node in nodelist:
       graph.add_node(nodelist[node])
   #Create Edges
   print "Building Edges"
   edgelist=[]
   for edge in edges:
       n1=nodelist[edge[0]]
       n2=nodelist[edge[1]]
       edgelist.append(makeedge(n1,n2,edge[2]))

   #Add Edges
   print "Adding Edges"
   for edge in edgelist:
      graph.add_edge(edge)

   #output graph
   print "Writing Graph"
   graph.write_png(outfile)
   
   #output Stats
   print "%d Nodes" % len(nodelist)
   print "%d Dependencies" % len(edgelist)
   print "%d Cluster" % len(clusterlist)

