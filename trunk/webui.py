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
    depslist = dg.depstrings(dgconf.GeneralOptions)
    newdeps = []
    for depline in depslist.deps:
        if depline['resource'] in ta['deps']:
            newdeps.append(depline)
    depslist.deps = newdeps
    print newdeps
    depslist.clusters = depslist.getclusters(depslist.deps)
    depslist.edges = depslist.getedges(depslist.deps)
    depslist.nodes = depslist.getnodes(depslist.deps)
    print depslist.nodes
    dgconf.GeneralOptions['outfile'] = 'maps/' + system + '.png'
    buildgraph(dgconf, depslist)
    out = template('systempage', deps = ta['deps'], system = system)
    return out

@route('/maps/<path:path>')
def callback(path):
    return static_file(path, root = './maps/')

dgconf = dg.depconfig()
deplist = dg.depstrings(dgconf.GeneralOptions)

if __name__ == '__main__':
    run(host = 'localhost', port = 8080, debug = True)
