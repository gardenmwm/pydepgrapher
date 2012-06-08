from bottle import route, run, template, static_file
from pydepgrapher import *
import dg


@route('/')
def base():
    output = template('overall', systems = deplist.nodes)
    return output

@route('/:system')
def systempage(system):
    ta = {'system':system}
    ta['deps'] = dg.getdepnodes(system, deplist.deps)
    ta['reqs'] = dg.getnodedeps(system, deplist.deps)
    #Create Deplist and graph
    depslist = dg.depstrings(dgconf.GeneralOptions)
    newdeps = []
    for depline in depslist.deps:
        if depline['resource'] in ta['deps']:
            newdeps.append(depline)
    for depline in newdeps:
        if depline['dependency'] not in ta['deps']:
            depline['dependency'] = ''
    depslist.deps = newdeps
    depslist.clusters = depslist.getclusters(depslist.deps)
    depslist.edges = depslist.getedges(depslist.deps)
    depslist.nodes = depslist.getnodes(depslist.deps)
    dgconf.GeneralOptions['outfile'] = 'maps/deps' + system + '.png'
    buildgraph(dgconf, depslist)
    #Create ReqList
    reqslist = dg.depstrings(dgconf.GeneralOptions)
    newreqs = []
    for depline in reqslist.deps:
        if depline['resource'] in ta['reqs']:
            newreqs.append(depline)
    #for depline in newreqs:
    #    if depline['resource'] not in ta['reqs']:
    #        depline['resource'] = ''
    depslist.deps = newreqs
    depslist.clusters = depslist.getclusters(depslist.deps)
    depslist.edges = depslist.getedges(depslist.deps)
    depslist.nodes = depslist.getnodes(depslist.deps)
    dgconf.GeneralOptions['outfile'] = 'maps/reqs' + system + '.png'
    buildgraph(dgconf, depslist)
    out = template('systempage', deps = ta['deps'], reqs = ta['reqs'], system = system)
    return out

@route('/maps/<path:path>')
def callback(path):
    return static_file(path, root = './maps/')

dgconf = dg.depconfig()
deplist = dg.depstrings(dgconf.GeneralOptions)

if __name__ == '__main__':
    run(host = '159.36.2.46', port = 8080, debug = True)
