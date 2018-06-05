# row function
# column name-> Facet -> Text facet
# Method: key collision   Keying Function: fingerprint
# json file: ********
# operation_name: "core/mass-edit"
# description: "Mass edit cells in column name"
# engineConfig: { mode:"row_based" facets: "[]"}
# column_name: "name"
# expression: "value"
# edits: {"fromBlank","fromError","from","to"}
import json
from pprint import pprint

with open('OpenRefineTest.json') as json_data:
    data=json.load(json_data)


operation={}
operation['operation_name']=[]
operation['method_name']=[]
operation['target']=[]

for d in data:
    try:
        operation['operation_name'].append(d['op'])
        operation['method_name'].append(d['expression'])
    except KeyError:
        pass

edits=[]
for d in data:
    try:
        edits+=d['edits']
    except KeyError:
        pass

for e in edits:
    operation['target'].append(e['to'])

pprint(operation)


