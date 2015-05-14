**News**
Now supports clusters, look at the latest in the code repo

I kept looking for a tool that would easily let me graph the dependencies of my networks, and be easy for anyone else to modify. So I created this tool which takes a csv file of nodes and their dependencies, then uses pyDot and Graphviz to make pretty graphs.

pyDepGrapher turns this;
```
resource,resource_type,dependency,dependency_type,cluster
athena,Mac,NetGear2200,nfs,
NetGear2200,NAS,,,
aphrodite,RHEL_Server,NetGear2200,nfs,HA_Cluster
athena,,airport,dns,
aphrodite,,airport,dns,
hera,Windows7,airport,dns,
hera,,aphrodite,SMB,
hera,,NetGear2200,nfs,
phoebe,RHEL_Server,aphrodite,SMB,HA_Cluster
phoebe,,airport,dns,
phoebe,,NetGear2200,nfs,
```

into this

---

![http://six9s.com/depchart.png](http://six9s.com/depchart.png)