# @begin OpenRefine2YW
# @in data_path @as json_path @uri file:data.json
# @out operation @as operation_dictionary

import json
from pprint import pprint
import pandas as pd

# @begin import_json
# @in json_path
# @out data @as raw_json_file
with open('data_review.json') as json_data:
    data=json.load(json_data)

# @end import_json

# @begin extract_operation @desc Output a dictionary to store the operation name, method and target in details
# @in raw_json_file
# @out operation_dictionary
operation={}
operation['operation_name']=[]
operation['method_name']=[]
operation['target']=[]
operation['cluster']=[]

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
    operation['cluster'].append(e['Method']+' '+e['Keying Function'])

data_review={}
data_review['cluster']=[]
data_review['to']=[]
data_review['cluster'].append(operation['cluster'])
data_review['to'].append(operation['target'])

df=pd.DataFrame(data=data_review)
print(df)

with open('json_review.txt','w+')as f:
    f.write('operation_name:'+'\n')
    for op in operation['operation_name']:
        f.write(str(op+'\n'))
    f.write('method:'+'\n')
    for me in operation['method_name']:
        f.write(str(me)+'\n')
    f.write('cluster:'+'\n')
    for cl in operation['cluster']:
        f.write(str(cl)+'\n')

    f.write('target:'+'\n')
    for ta in operation['target']:
        f.write(str(ta)+'\n')



# @end extract_operation


# @end OpenRefine2YW
