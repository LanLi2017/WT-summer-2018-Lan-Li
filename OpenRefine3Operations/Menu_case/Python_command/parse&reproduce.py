import json
from pprint import pprint

# create
from OpenRefine3Operations.Menu_case.Python_command import OpenRefinerecipe


# def create_op(data):
#     for dicts in data:
#         if dicts['op']=='create':
#             projectID=dicts['projectID']
#             print(type(projectID))
#             projectName=dicts['projectName']
#             print(type(projectName))
#             project_path=dicts['projectPath']
#             return OpenRefinerecipe.create_project(project_path,projectName)


# rename
def rename_op(data,projectID):
    for dicts in data:
        if dicts['opname']=='rename':
            oldcol=dicts['oldColumnName']
            newcol=dicts['newColumnName']
            print(oldcol)
            print(newcol)
            return OpenRefinerecipe.rename_column(projectID,oldcol,newcol)


# cluster and relabel
'''
{
"op": "core/mass-edit",
"opname": "Cluster and Relabel",
"description:": "Mass edit cells in column Event ",
"engineConfig": {"mode": "row-based","facets": []},
"columnName": "Event",
"expression": "value",
"type": "binning", 
"function": "fingerprint",
"params": 20
}
'''
def clusterAndrelabel(data,projectID):
    for dicts in data:
        if dicts['opname']=='Cluster and Relabel':
            columnName=dicts['columnName']
            clusterer_type=dicts['type']
            function=dicts['function']
            params=dicts['params']
            # what if people choose different clusters?
            return OpenRefinerecipe.compute_clusters(projectID,columnName,clusterer_type=clusterer_type,function=function,params=params)



# trim whitespace
'''
{
"op": "core/text-transform",
"opname": "TrimwhiteSpace",
"description": "Text transform on cells in column Event using expression value.trim()",
"engineConfig": {"mode": "row-based","facets": []},
"columnName": "Event",
"expression": "value.trim()",
"onError": "set-to-blank",
"repeat": false,
"repeatCount": 10
}
'''
def trim_op(data,projectID):
    for dicts in data:
        if dicts['opname']=='TrimwhiteSpace':
            columnName=dicts['columnName']
            expression=dicts['expression']
            return OpenRefinerecipe.text_transform(projectID,columnName,expression)



# lowercase
'''
{
"op": "core/text-transform",
"opname": "toLowercase",
"description": "Text transform on cells in column Event using expression value.toLowercase()",
"engineConfig": {"mode": "row-based","facets": []},
"columnName": "Event",
"expression": "value.toLowercase()",
"onError": "set-to-blank",
"repeat": false,
"repeatCount": 10
}

'''
def lowercase_op(data,projectID):
    for dicts in data:
        if dicts['opname']=='toLowercase':
            columnName=dicts['columnName']
            expression=dicts['expression']
            return OpenRefinerecipe.text_transform(projectID,columnName,expression)

# uppercase
'''
{
    "op": "core/text-transform",
    "opname": "toUppercase",
    "description": "Text transform on cells in column date using expression value.toUppercase()",
    "engineConfig": {
      "mode": "row-based",
      "facets": []
    },
    "columnName": "sponsor",
    "expression": "value.toUppercase()",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  }
'''
def uppercase_op(data,projectID):
    for dicts in data:
        if dicts['opname']=='toUppercase':
            columnName=dicts['columnName']
            expression=dicts['expression']
            return OpenRefinerecipe.text_transform(projectID,columnName,expression)



# Todate
'''
{
    "op": "core/text-transform",
    "opname": "toDate",
    "description": "Text transform on cells in column date using expression value.toDate()",
    "engineConfig": {
      "mode": "row-based",
      "facets": []
    },
    "columnName": "date",
    "expression": "value.toDate()",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  }
'''
def Todate_op(data,projectID):
    for dicts in data:
        if dicts['opname']=='toDate':
            columnName=dicts['columnName']
            expression=dicts['expression']
            return OpenRefinerecipe.text_transform(projectID,columnName,expression)


# ToNumber
'''
{
    "op": "core/text-transform",
    "op": "toNumber",
    "description": "Text transform on cells in column date using expression value.toNumber()",
    "engineConfig": {
      "mode": "row-based",
      "facets": []
    },
    "columnName": "dish_count",
    "expression": "value.toNumber()",
    "onError": "set-to-blank",
    "repeat": false,
    "repeatCount": 10
  }

'''
def Tonumber_op(data,projectID):
    for dicts in data:
        if dicts['opname']=='toNumber':
            columnName=dicts['columnName']
            expression=dicts['expression']
            return OpenRefinerecipe.text_transform(projectID,columnName,expression)



# split
'''
[
  {
    "op": "core/column-split",
    "opname": "Splitcolumn",
    "description": "Split column call_number by separator",
    "engineConfig": {
      "mode": "row-based",
      "facets": []
    },
    "columnName": "call_number",
    "guessCellType": true,
    "removeOriginalColumn": true,
    "mode": "separator",
    "separator": " ",
    "regex": false,
    "maxColumns": 0
  }
]
'''
def Split_op(data,projectID):
    for dicts in data:
        if dicts['opname']=='Splitcolumn':
            columnName=dicts['columnName']
            separator=dicts['separator']
            return OpenRefinerecipe.split_column(projectID,columnName,separator)
    pass



def main():
    project_Name=raw_input('Enter the project name:\n')
    project_path=raw_input('Enter the project path:\n')
    projectID=OpenRefinerecipe.create_project(project_path,project_Name)
    with open('TlogWorkflow.json','r')as f:
        dataset=json.load(f)
    print(dataset)
    i=0
    while True:
        rename_op(dataset,projectID)
        clusterAndrelabel(dataset,projectID)
        lowercase_op(dataset,projectID)
        uppercase_op(dataset,projectID)
        Tonumber_op(dataset,projectID)
        Todate_op(dataset,projectID)
        trim_op(dataset,projectID)
        Split_op(dataset,projectID)
        i=i+1



if __name__=='__main__':
    main()



