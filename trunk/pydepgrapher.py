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
import csv
import ConfigParser
import sys

def GetNodeOptions(parser):
    Opts={}
    NodeOpts={}
    #Get Node Types
    NodeTypes=parser.get('types', 'NodeTypes').split(',')
    for nt in NodeTypes:
        #Only pull options for ones that have sections
        if parser.has_section(nt):
            for name,value in parser.items(nt):
                NodeOpts[name]=value
            Opts[nt]=NodeOpts
            NodeOpts={}
    #print Opts
    return Opts

def GetEdgeOptions(parser):
    Opts={}
    EdgeOpts={}
    #Get Node Types
    EdgeTypes=parser.get('types', 'DepTypes').split(',')
    for et in EdgeTypes:
        #Only pull options for ones that have sections
        if parser.has_section(et):
            for name,value in parser.items(et):
                EdgeOpts[name]=value
            Opts[et]=EdgeOpts
            EdgeOpts={}
    #print Opts
    return Opts

def GetGraphOptions(parser):
    Opts={}
    Opts['graph_type']='digraph'
    for name,value in parser.items('graph'):
        Opts[name]=value
    return Opts

def readsource(sourcefile):
    deplist=[]
    f=open(sourcefile,'rt')
    reader = csv.DictReader(f)
    for row in reader:
        deplist.append(row)
    return deplist

def getnodes(deps):
    nodelist={}
    for dep in deps:
        nodelist[dep['resource']]=dep['resource_type']
        if  dep['dependency'] not in nodelist and dep['dependency'] != '':
	       nodelist[dep['dependency']]=''
    return nodelist

def getclusters(deps):
    clusters={}
    for dep in deps:
        if dep['cluster'] != '' and dep['cluster'] in clusters:
            clusters[dep['cluster']].append(dep['resource'])
        elif dep['cluster'] != '' and dep['cluster'] not in clusters:
            clusters[dep['cluster']]=[dep['resource']]
    return clusters

def getedges(deps):
    edgelist=[]
    for dep in deps:
        if dep['dependency'] != '':
            edge=[dep['resource'],dep['dependency'],dep['dependency_type']]
            edgelist.append(edge)
    return edgelist

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

def getdepnodes(node,deps,depth=100):
    '''This will return a list of node strings that are dependant on this node, or an upwards direction'''
    nodelist=[node]
    while depth > 0:
        depth -= 1
        for dep in deps:
            if dep['dependency'] in nodelist and dep['resource'] not in nodelist:
                nodelist.append(dep['resource'])
    return nodelist

def getnodedeps(node,deps,depth=100):
    '''This will return a list of nodes that the specified node is dependent on, or a downwards direction'''
    nodelist=[node]
    while depth > 0:
        depth -= 1
        for dep in deps:
            if dep['resource'] in nodelist and dep['dependency'] not in nodelist:
                nodelist.append(dep['dependency'])
    return nodelist

if __name__=="__main__":
   #Parse Config
   print "Parsing Config"
   parser = ConfigParser.SafeConfigParser()
   parser.read('config.ini')
   sourcefile=parser.get('general', 'sourcefile')
   outfile=parser.get('general','outfile')
   NodeOptions=GetNodeOptions(parser)
   EdgeOptions=GetEdgeOptions(parser)
   GraphOptions=GetGraphOptions(parser)
   #Get Deps from file and into memory
   print "Reading Dep file"
   deps=readsource(sourcefile)
   print "Reading Nodes"
   nodestrings=getnodes(deps)
   print "Reading Edges"
   edges=getedges(deps)
   clusterstrings=getclusters(deps)
   
   #Build Nodes
   print "Building Nodes"
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

