# @begin OpenRefine2YW
# @in data_path @as json_path @uri file:data.json
# @out operation_name
# @out operation_method_name
# @out operation_target
import json
from pprint import pprint

# @begin import_json
# @in json_path @uri file:data.json
# @out data @as raw_json_file
with open('data.json') as json_data:
    data=json.load(json_data)

# @end import_json

# @begin extract_operation @desc Output a dictionary to store the operation name, method and target in details
# @in raw_json_file
# @out operation_name
# @out operation_method_name
# @out operation_target
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

# @end extract_operation


# @end OpenRefine2YW
