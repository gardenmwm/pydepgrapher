import ConfigParser
import csv

class depconfig(object):
    def __init__(self,config_file='config.ini'):
        parser = ConfigParser.SafeConfigParser()
        parser.read(config_file)
        self.NodeOptions=GetNodeOptions(parser)
        self.EdgeOptions=GetEdgeOptions(parser)
        self.GraphOptions=GetGraphOptions(parser)
        self.GeneralOptions['sourcefile']=parser.get('general', 'sourcefile')
        self.GeneralOptions['outfile']=parser.get('general','outfile')

    def GetNodeOptions(parser):
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

    def GetEdgeOptions(parser):
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
    
    def GetGraphOptions(parser):
        Opts={}
        Opts['graph_type']='digraph'
        for name,value in parser.items('graph'):
            Opts[name]=value
        return Opts
    
class depstrings(self):
    def __init__(self,GeneralOptions):
        self.deps=readsource(self.GeneralOptions['sourcefile'])
        self.nodes=getnodes(self.deps)
        self.edges=getedges(self.deps)
        self.clusterstrings=getclusters(self.deps)
        return
    
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