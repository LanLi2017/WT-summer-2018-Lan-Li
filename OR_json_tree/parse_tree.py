import json

import sys


data=open('OpenRefine.json').read()
data=json.loads(data)
print(json.dumps(data, indent=4), file=sys.stderr)

# extract tree edges from the dict
edges=[]

def get_edges(treedict, parent=None):
    name=next(iter(treedict.keys()))
    if parent is not None:
        edges.append((parent,name))
    for item in treedict[name]["children"]:
        if isinstance(item,dict):
            get_edges(item,parent=name)
        else:
            edges.append((name, item))


get_edges(data)
print('strict digraph tree{')
for row in edges:
    print('    {0} -> {1};'.format(*row))
print('}')
