# @begin OpenRefine2YW
# @in data_path @as json_path @uri:data.json


import json
from pprint import pprint

# @begin import_json
# @in json_path @uri data.json
# @out data @as raw_json_file
with open('data.json') as json_data:
    data=json.load(json_data)

# @end import_json

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

# df=pd.DataFrame(data=operation)
# print(df)


# @end OpenRefine2YW
