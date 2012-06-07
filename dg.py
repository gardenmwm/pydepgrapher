import ConfigParser
import csv

class depconfig(object):
    def __init__(self,config_file='config.ini'):
        parser = ConfigParser.SafeConfigParser()
        parser.read(config_file)
        self.GeneralOptions = {}
        self.NodeOptions = self.GetNodeOptions( parser )
        self.EdgeOptions = self.GetEdgeOptions( parser )
        self.GraphOptions = self.GetGraphOptions( parser )
        self.GeneralOptions['sourcefile']=parser.get('general', 'sourcefile')
        self.GeneralOptions['outfile']=parser.get('general','outfile')

    def GetNodeOptions( self, parser ):
        Opts={}
        NodeOpts={}
        NodeTypes=parser.get('types', 'NodeTypes').split(',')
        for nt in NodeTypes:
            #Only pull options for ones that have sections
            if parser.has_section(nt):
                for name,value in parser.items(nt):
                    NodeOpts[name]=value
                Opts[nt]=NodeOpts
                NodeOpts={}
        return Opts

    def GetEdgeOptions( self, parser ):
        Opts={}
        EdgeOpts={}
        EdgeTypes=parser.get('types', 'DepTypes').split(',')
        for et in EdgeTypes:
            #Only pull options for ones that have sections
            if parser.has_section(et):
                for name,value in parser.items(et):
                    EdgeOpts[name]=value
                Opts[et]=EdgeOpts
                EdgeOpts={}
        return Opts
    
    def GetGraphOptions( self, parser ):
        Opts={}
        Opts['graph_type']='digraph'
        for name,value in parser.items('graph'):
            Opts[name]=value
        return Opts


class depstrings(object):
    def __init__(self,GeneralOptions):
        self.deps = self.readsource( GeneralOptions['sourcefile'] )
        self.nodes = self.getnodes( self.deps )
        self.edges = self.getedges( self.deps )
        self.clusters = self.getclusters( self.deps )
        return
    
    def readsource( self, sourcefile ):
        deplist=[]
        f=open(sourcefile,'rt')
        reader = csv.DictReader(f)
        for row in reader:
            deplist.append(row)
        return deplist
    
    def getnodes( self, deps ):
        nodelist={}
        for dep in deps:
            nodelist[dep['resource']]=dep['resource_type']
            if  dep['dependency'] not in nodelist and dep['dependency'] != '':
               nodelist[dep['dependency']]=''
        return nodelist
    
    def getclusters( self, deps ):
        clusters={}
        for dep in deps:
            if dep['cluster'] != '' and dep['cluster'] in clusters:
                clusters[dep['cluster']].append(dep['resource'])
            elif dep['cluster'] != '' and dep['cluster'] not in clusters:
                clusters[dep['cluster']]=[dep['resource']]
        return clusters
    
    def getedges( self, deps ):
        edgelist=[]
        for dep in deps:
            if dep['dependency'] != '':
                edge=[dep['resource'],dep['dependency'],dep['dependency_type']]
                edgelist.append(edge)
        return edgelist

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
