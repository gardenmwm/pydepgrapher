#!/usr/bin/python
'''
pyDepGrapher

This program creates graphs of from a list of dependencies provided in a csv
file. 
It uses graphviz and pydot heavily. 

Copyright (c) 2012-2018 Matt Marshall <gardenmwm@gmail.com>
Distributed under MIT licesne

pyDepGrapher Homepage: 	http://code.google.com/p/pydepgrapher/
pydot:			http://code.google.com/p/pydot/
Graphviz		http://www.graphviz.org
@author: gardenmwm
'''
import pydot
import csv
import ConfigParser

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

def NodeExistsInList(nodelist,nodestring):
    found = False
    i=0
    for node in nodelist:
        if nodestring == node[0]: found = i
        i+=1
    return found

def getnodes(deps):
    nodelist=[]
    for dep in deps:
        if not NodeExistsInList(nodelist,dep['resource']):
            nodelist.append([dep['resource'],dep['resource_type']])
        elif dep['resource_type'] != '':
            nodelist[NodeExistsInList(nodelist,dep['resource'])][1]=dep['resource_type']
        if not NodeExistsInList(nodelist,dep['dependancy']) and dep['dependancy'] != '':
            nodelist.append([dep['dependancy'],''])
    return nodelist

def getedges(deps):
    edgelist=[]
    for dep in deps:
        if dep['dependancy'] != '':
            edge=[dep['resource'],dep['dependancy'],dep['dependancy_type']]
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

#Build Nodes
print "Building Nodes"
nodelist=[]
for node in nodestrings:
    nodelist.append(makenode(node[0],node[1]))

#create graph and add nodes
graph=pydot.Dot(**GraphOptions)
#graph=pydot.Dot(graph_type='digraph',ratio=1.3,layout='dot',sep='+1',overlap='scalexy')
print "Adding Nodes"
for node in nodelist:
    graph.add_node(node)

#Create Edges
print "Building Edges"
edgelist=[]
for edge in edges:
    n1=graph.get_node(edge[0])[0]
    n2=graph.get_node(edge[1])[0]
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
    

