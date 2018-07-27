import json
from pprint import pprint


__author__='Lan Li'
# create
import OpenRefinerecipe





def main():
    project_Name=raw_input('Enter the project name:\n')
    project_path=raw_input('Enter the input dataset path:\n')
    projectID=OpenRefinerecipe.create_project(project_path,project_Name)
        # dataset=json.load(f)
    # for further change :
    '''
    1.original 
    2.Extended
    3.combine
    '''
    with open('ExtendedWF.json','r')as f:
        dataset=json.load(f)
    print(dataset)
    '''
    
    
    '''
    for dicts in dataset:
        if dicts['opname']=='rename':
            oldcol=dicts['oldColumnName']
            newcol=dicts['newColumnName']
            OpenRefinerecipe.rename_column(projectID,oldcol,newcol)
        elif dicts['opname']=='Cluster_and_Relabel':
            '''
            {
            "Cluster-function": "fingerprint", 
            "description": "Mass edit cells in column sponsor", 
            "Cluster-params": "20", 
            "columnName": "sponsor", 
            "engineConfig": {
              "facets": "[]", 
              "mode": "row-based"
            }, 
            "opname": "Cluster_and_Relabel", 
            "Cluster-type": "binning", 
            "expression": "value", 
            "op": "core/mass-edit"
          }, 
            
            '''
            columnName=dicts['columnName']
            clusterer_type=dicts['Cluster-type']
            function=dicts['Cluster-function']
            params=dicts['Cluster-params']
            # what if people choose different clusters?
            compute_clusters=OpenRefinerecipe.compute_clusters(projectID,columnName,clusterer_type=clusterer_type,function=function,params=params)
            Edit_from=OpenRefinerecipe.getFromValue(compute_clusters)
            Edit_to=OpenRefinerecipe.getToValue(compute_clusters)
            edits=[{'from':f1, 'to':t} for f1,t in zip(Edit_from, Edit_to)]
            OpenRefinerecipe.mass_edit(projectID,columnName,edits)


        elif dicts['op']=='core/text-transform':
            '''
            {
            "repeat": "false", 
            "description": "Text transform on cells in column sponsor using expression value.trim()", 
            "onError": "set-to-blank", 
            "repeatCount": 10, 
            "columnName": "sponsor", 
            "engineConfig": {
              "facets": "[]", 
              "mode": "row-based"
            }, 
            "opname": "TrimwhiteSpace", 
            "expression": "value.trim()", 
            "op": "core/text-transform"
          }, 
        
            '''
            columnName=dicts['columnName']
            expression=dicts['expression']
            OpenRefinerecipe.text_transform(projectID,columnName,expression)
        elif dicts['opname']=='Splitcolumn':
            '''
            {
            "regex": "false", 
            "description": "Split column call_number by separator", 
            "maxColumns": 0, 
            "columnName": "call_number", 
            "guessCellType": "true", 
            "removeOriginalColumn": "true", 
            "separator": " ", 
            "mode": "separator", 
            "engineConfig": {
              "facets": "[]", 
              "mode": "row-based"
            }, 
            "opname": "Splitcolumn", 
            "op": "core/column-split"
          }
            
            '''
            columnName=dicts['columnName']
            separator=dicts['separator']
            OpenRefinerecipe.split_column(projectID,columnName,separator)




if __name__=='__main__':
    main()



