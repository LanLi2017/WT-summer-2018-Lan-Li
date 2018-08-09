# coding=utf-8
import csv
import json

# import sys
# sys.path.append('/Users/barbaralee/WT-summer-2018-Lan-Li/OpenRefine3Operations/Menu_case/Python_command/Openrefine-client reproducible json/script')
import OpenRefinerecipe

import subprocess


# get yes or no to continue
def Confirm(message,default=None):
    while True:
        if default is None:
            message += ' (y/n)'
        elif default:
            # set Yes as default
            message += ' (Y/n)'
        else:
            # set No as default
            message += ' (y/N)'

        input_str=raw_input(message).lower()
        # if no input :
        if default is not None and not input_str:
            return default
        elif input_str == 'y':
            return True
        elif input_str == 'n':
            return False


def prompt_int(message, min=None, max=None):
    while True:
        input_str = raw_input(message)

        try:
            value = int(input_str)

            if min is not None and value < min:
                raise ValueError
            if max is not None and value > max:
                raise ValueError

        except ValueError:
            pass
        else:
            return value


# Choice with corresponding index
def prompt_options(options):
    for idx, option in enumerate(options, start=1):
        print(idx, option)

    if not options:
        return 0
    else:
        return prompt_int('Please enter your choice: ', min=1, max=len(options))


def GetColumnName(projectID):
    response=OpenRefinerecipe.get_models(projectID)
    column_model = response['columnModel']
    column_name = [column['name'] for column in column_model['columns']]
    return column_name


def checkpath():
    while True:
        try:
            path=raw_input("Enter the input file path: ")
            with open(path,'r')as f:
                f.close()
        except IOError as e:
            print(e)
        else:
            return path


def main():
    result=[]
    print("Welcome to use OpenRefine userScript")
    # import project
    while True:
        choice=prompt_options([
            'List Projects',
            'Create Project',
            'Open Project',
            'Get Project Name',
            'Exit',
        ])
        if choice==1:
            OpenRefinerecipe.list_objects()
        elif choice==3:
            userinputID=raw_input("input the project ID:")
            OpenRefinerecipe.open_project(userinputID)
            # f.write('Open Project')
        elif choice==4:
            usergetprojectID=raw_input("input the project ID:")
            OpenRefinerecipe.get_project_name(usergetprojectID)
            # f.write('Get Project Name')
        elif choice==2:
            # f.write('Create Project')
            # while True:
            #     try:
            #         userinputpath=raw_input("input the file path:")
            #         with open(userinputpath,'r')
            userinputpath=checkpath()
            userinputName=raw_input("input the project Name:")

            # createdicts ={}
            # createdicts['op']='createProject'
            # createdicts['opname']='create'
            # createdicts['description']='create a new project'
            # createdicts['projectName']='%s'%userinputName
            # createdicts['projectPath']='%s'%userinputpath
            # f.write('@IN file path: %s'%userinputpath)
            # f.write('@IN project Name: %s'%userinputName)
            projectID=OpenRefinerecipe.create_project(userinputpath,userinputName)
            # createdicts['projectID']='%s'%projectID
            # result.append(createdicts)
            # f.write('@OUT New Project ID : %s'%projectID)

            number_rows=raw_input("Display some number of rows: You can choose 5/10/25/50")
            print("Show the first "+number_rows+" rows for this project:")

            with open(userinputpath,'rb') as project:
                content=tuple(project)
                header=content[0]
                print(header)
                # data=tuple(content[1:int(number_rows)+1])
                for i in range(1,int(number_rows)+1):
                    print(content[i])


            '''
            rename operation
            [
              {
                "op": "core/column-rename",
                "description": "Rename column currency to money",
                "oldColumnName": "currency",
                "newColumnName": "money"
              }
            ]
            
            '''

            userrenamechoice=raw_input("Enter the column name you want to change, if there is no choice , please enter N: ")
            while userrenamechoice!='N':
                renamedicts={}
                renamedicts['op']='core/column-rename'
                renamedicts['opname']='rename'
                newcolumnname=raw_input("Enter the new column name:")
                renamedicts['description']='Rename column %s to %s'%(userrenamechoice, newcolumnname)
                renamedicts['oldColumnName']='%s'%userrenamechoice
                renamedicts['newColumnName']='%s'%newcolumnname
                result.append(renamedicts)
                OpenRefinerecipe.rename_column(projectID,userrenamechoice,newcolumnname)
                userrenamechoice=raw_input("Continue Enter the column name you want to change, if there is no choice, please Enter N: ")

            # split row mode and record mode
            print(GetColumnName(projectID))
            usercolumn=raw_input("Enter the column name you want to do Data Wrangling,if there is no other columns you want to make change, enter N: ")
            while usercolumn!='N':
                # f.write('Data Wrangling On Column %s'%usercolumn)
                while True:
                    userMode=prompt_options([
                        'row mode',
                        'record mode',
                        'Exit',
                    ])
                    if userMode==2:
                        # f.write('Record mode ')
                        # five steps
                        # 1. identify the field that contains the records marker
                        userStandardColumn=raw_input("Please input the records marker: ")
                        # 2. move this field as the first column
                        OpenRefinerecipe.reorder_columns(projectID,0)
                        # 3. sort this column (no corresponding function)
                    elif userMode==1:
                            # f.write('Row mode ')
                            while True:
                                userOperates=prompt_options([
                                    'Cluster and Relabel',
                                    'Trim Whitespace',
                                    'Lowercase the column value',
                                    'Uppercase the column value',
                                    'Transform the column value to Date',
                                    'Transform the column value to Numeric',
                                    'Split multi-valued cells in column ',
                                    'Exit',
                                ])
                                if userOperates==1:
                                    '''
                                    {
                                    "op": "core/mass-edit",
                                    "description": "Mass edit cells in column sponsor",
                                    "engineConfig": {
                                      "mode": "row-based",
                                      "facets": []
                                    },
                                    "columnName": "sponsor",
                                    "expression": "value",
                                    "edits": [
                                     {
                                        "fromBlank": false,
                                        "fromError": false,
                                        "from": [
                                          "waldorf astoria",
                                          "waldorf-astoria"
                                        ],
                                        "to": "waldorf astoria"
                                      }
                                    ]
                                  },
                                    
                                    
                                    '''
                                    ClusterRelabeldicts={}
                                    ClusterRelabeldicts['op']='core/mass-edit'
                                    ClusterRelabeldicts['opname']='Cluster_and_Relabel'
                                    ClusterRelabeldicts['description']='Mass edit cells in column %s'%usercolumn
                                    ClusterRelabeldicts['engineConfig']={}
                                    ClusterRelabeldicts['engineConfig']['mode']='row-based'
                                    ClusterRelabeldicts['engineConfig']['facets']='[]'
                                    ClusterRelabeldicts['columnName']='%s'%usercolumn
                                    ClusterRelabeldicts['expression']='value'

                                    # print("please choose clustering type:")
                                    print("1. binning")
                                    print("2. knn")
                                    userClusterer=raw_input("please choose clustering type:")
                                    if userClusterer=='1':
                                        ClusterRelabeldicts['Cluster-type']='binning'
                                        userFunction=prompt_options([
                                            'fingerprint',
                                            'metaphone3',
                                            'cologne-phonetic',
                                        ])
                                        if userFunction==1:
                                            ClusterRelabeldicts['Cluster-function']='fingerprint'
                                            params=raw_input("Enter the params:")
                                            ClusterRelabeldicts['Cluster-params']='%s'%params
                                            result.append(ClusterRelabeldicts)
                                            compute_clusters=OpenRefinerecipe.compute_clusters(projectID,usercolumn,clusterer_type='binning',function='ngram-fingerprint',params=params)
                                        elif userFunction==2:
                                            ClusterRelabeldicts['Cluster-function']='metaphone3'
                                            result.append(ClusterRelabeldicts)
                                            compute_clusters=OpenRefinerecipe.compute_clusters(projectID,usercolumn,clusterer_type='binning',function='metaphone3')
                                        elif userFunction==3:
                                            ClusterRelabeldicts['Cluster-function']='cologne-phonetic'
                                            result.append(ClusterRelabeldicts)
                                            compute_clusters=OpenRefinerecipe.compute_clusters(projectID,usercolumn,clusterer_type='binning',function='cologne-phonetic')

                                    elif userClusterer=='2':
                                        ClusterRelabeldicts['Cluster-type']='knn'
                                        userKNNfunction=prompt_options([
                                           'levenshtein',
                                           'PPM',
                                        ])
                                        if userKNNfunction==1:
                                            ClusterRelabeldicts['Cluster-function']='levenshtein'
                                            print("Please set the params: ")
                                            userinputradius=float(raw_input("Set the radius: "))
                                            userinputNgramsize=int(raw_input("Set the Bloking Ngram-size: "))
                                            ClusterRelabeldicts['Cluster-params']='{"radius":%f, "blocking-ngram-size":%d}'%(userinputradius,userinputNgramsize)
                                            result.append(ClusterRelabeldicts)
                                            compute_clusters=OpenRefinerecipe.compute_clusters(projectID,usercolumn,clusterer_type='knn',function='levenshtein',params={ 'radius':userinputradius,'blocking-ngram-size':userinputNgramsize})
                                        elif userKNNfunction==2:
                                            ClusterRelabeldicts['Cluster-function']='PPM'
                                            print("Please set the params: ")
                                            userinputradius=float(raw_input("Set the radius: "))
                                            userinputNgramsize=int(raw_input("Set the Bloking Ngram-size: "))
                                            ClusterRelabeldicts['Cluster-params']='{"radius":%f, "blocking-ngram-size":%d}'%(userinputradius,userinputNgramsize)
                                            result.append(ClusterRelabeldicts)
                                            compute_clusters=OpenRefinerecipe.compute_clusters(projectID,usercolumn,clusterer_type='knn',function='PPM',params={ 'radius':userinputradius,'blocking-ngram-size':userinputNgramsize})
                                    print(compute_clusters)
                                    userClusterinput=raw_input("Do you want to do manually edition for cluster? If not, input N; else input Y: ")

                                    Edit_from=OpenRefinerecipe.getFromValue(compute_clusters)
                                    Edit_to=OpenRefinerecipe.getToValue(compute_clusters)
                                    if userClusterinput =='N':
                                        edits=[{'from':f1, 'to':t} for f1,t in zip(Edit_from, Edit_to)]
                                        print(edits)
                                        ClusterRelabeldicts['edits']=edits
                                        OpenRefinerecipe.mass_edit(projectID,usercolumn,edits,expression='value')
                                    elif userClusterinput=='Y':
                                        print("This is the original values in cluster: ")
                                        print(Edit_from)
                                        print("This is the values after the chosen cluster: ")
                                        print(Edit_to)
                                        Edit_new_to=[]
                                        for to in Edit_to:
                                            print(to)
                                            userinputTo=raw_input("Input the value you want to make change with this value, if not, input N")
                                            if userinputTo!='N':

                                                to=userinputTo
                                                Edit_new_to.append(to)
                                            else:
                                                to=to
                                                Edit_new_to.append(to)
                                        print(Edit_new_to)
                                        mannually_edits=[{'from':f1, 'to':t} for f1,t in zip(Edit_from, Edit_new_to)]
                                        ClusterRelabeldicts['edits']=mannually_edits
                                        OpenRefinerecipe.mass_edit(projectID,usercolumn,mannually_edits,expression='value')

                                elif userOperates==2:
                                    '''
                                    {
                                    "op": "core/text-transform",
                                    "description": "Text transform on cells in column sponsor using expression value.trim()",
                                    "engineConfig": {
                                      "mode": "row-based",
                                      "facets": []
                                    },
                                    "columnName": "sponsor",
                                    "expression": "value.trim()",
                                    "onError": "set-to-blank",
                                    "repeat": false,
                                    "repeatCount": 10
                                  }
                                    '''
                                    trimdicts={}
                                    trimdicts['op']='core/text-transform'
                                    trimdicts['opname']='TrimwhiteSpace'
                                    trimdicts['description']='Text transform on cells in column %s using expression value.trim()'%usercolumn
                                    trimdicts['engineConfig']={}
                                    trimdicts['engineConfig']['mode']='row-based'
                                    trimdicts['engineConfig']['facets']='[]'
                                    trimdicts['columnName']='%s'%usercolumn
                                    trimdicts['expression']='value.trim()'
                                    trimdicts['onError']='set-to-blank'
                                    trimdicts['repeat']='false'
                                    trimdicts['repeatCount']=10
                                    result.append(trimdicts)

                                    OpenRefinerecipe.text_transform(projectID,usercolumn,'value.trim()')
                                elif userOperates==3:
                                    '''
                                    {
                                    "op": "core/text-transform",
                                    "description": "Text transform on cells in column sponsor using expression value.toLowercase()",
                                    "engineConfig": {
                                      "mode": "row-based",
                                      "facets": []
                                    },
                                    "columnName": "sponsor",
                                    "expression": "value.toLowercase()",
                                    "onError": "set-to-blank",
                                    "repeat": false,
                                    "repeatCount": 10
                                  }
                                    
                                    '''

                                    Lowercasedicts={}
                                    Lowercasedicts['op']='core/text-transform'
                                    Lowercasedicts['opname']='toLowercase'
                                    Lowercasedicts['description']='Text transform on cells in column %s using expression value.toLowercase()'%usercolumn
                                    Lowercasedicts['engineConfig']={}
                                    Lowercasedicts['engineConfig']['mode']='row-based'
                                    Lowercasedicts['engineConfig']['facets']='[]'
                                    Lowercasedicts['columnName']='%s'%usercolumn
                                    Lowercasedicts['expression']='value.toLowercase()'
                                    Lowercasedicts['onError']='set-to-blank'
                                    Lowercasedicts['repeat']='false'
                                    Lowercasedicts['repeatCount']=10
                                    result.append(Lowercasedicts)
                                    OpenRefinerecipe.text_transform(projectID,usercolumn,'value.toLowercase()')
                                elif userOperates==4:

                                    Uppercasedicts={}
                                    Uppercasedicts['op']='core/text-transform'
                                    Uppercasedicts['opname']='toUppercase'
                                    Uppercasedicts['description']='Text transform on cells in column %s using expression value.toUppercase()'%usercolumn
                                    Uppercasedicts['engineConfig']={}
                                    Uppercasedicts['engineConfig']['mode']='row-based'
                                    Uppercasedicts['engineConfig']['facets']='[]'
                                    Uppercasedicts['columnName']='%s'%usercolumn
                                    Uppercasedicts['expression']='value.toUppercase()'
                                    Uppercasedicts['onError']='set-to-blank'
                                    Uppercasedicts['repeat']='false'
                                    Uppercasedicts['repeatCount']=10
                                    result.append(Uppercasedicts)

                                    OpenRefinerecipe.text_transform(projectID,usercolumn,'value.toUppercase()')
                                elif userOperates==5:
                                    Datedicts={}
                                    Datedicts['op']='core/text-transform'
                                    Datedicts['opname']='ToDate'
                                    Datedicts['description']='Text transform on cells in column %s using expression value.toDate()'%usercolumn
                                    Datedicts['engineConfig']={}
                                    Datedicts['engineConfig']['mode']='row-based'
                                    Datedicts['engineConfig']['facets']='[]'
                                    Datedicts['columnName']='%s'%usercolumn
                                    Datedicts['expression']='value.toDate()'
                                    Datedicts['onError']='set-to-blank'
                                    Datedicts['repeat']='false'
                                    Datedicts['repeatCount']=10
                                    result.append(Datedicts)

                                    OpenRefinerecipe.text_transform(projectID,usercolumn,'value.toDate()')
                                elif userOperates==6:
                                    Numberdicts={}
                                    Numberdicts['op']='core/text-transform'
                                    Numberdicts['opname']='toNumber'
                                    Numberdicts['description']='Text transform on cells in column %s using expression value.toNumber()'%usercolumn
                                    Numberdicts['engineConfig']={}
                                    Numberdicts['engineConfig']['mode']='row-based'
                                    Numberdicts['engineConfig']['facets']='[]'
                                    Numberdicts['columnName']='%s'%usercolumn
                                    Numberdicts['expression']='value.toNumber()'
                                    Numberdicts['onError']='set-to-blank'
                                    Numberdicts['repeat']='false'
                                    Numberdicts['repeatCount']=10
                                    result.append(Numberdicts)

                                    OpenRefinerecipe.text_transform(projectID,usercolumn,'value.toNumber()')
                                elif userOperates==7:
                                    '''
                                    {
                                    "op": "core/column-split",
                                    "description": "Split column event by separator",
                                    "engineConfig": {
                                      "mode": "row-based",
                                      "facets": []
                                    },
                                    "columnName": "event",
                                    "guessCellType": true,
                                    "removeOriginalColumn": true,
                                    "mode": "separator",
                                    "separator": " ",
                                    "regex": false,
                                    "maxColumns": 0
                                  }
                                    
                                    '''
                                    Splitdicts={}
                                    Splitdicts['op']='core/column-split'
                                    Splitdicts['opname']='Splitcolumn'
                                    Splitdicts['description']='Split column %s by separator'%usercolumn
                                    Splitdicts['engineConfig']={}
                                    Splitdicts['engineConfig']['mode']='row-based'
                                    Splitdicts['engineConfig']['facets']='[]'
                                    Splitdicts['columnName']='%s'%usercolumn
                                    Splitdicts['guessCellType']='true'
                                    usersetremove=raw_input("Remove the original column or not,set true or false")
                                    Splitdicts['removeOriginalColumn']='%s'%usersetremove
                                    Splitdicts['mode']='separator'

                                    userSeparator=raw_input("input the separator: ")
                                    Splitdicts['separator']='%s'%userSeparator
                                    Splitdicts['regex']='false'
                                    Splitdicts['maxColumns']=0
                                    result.append(Splitdicts)
                                    OpenRefinerecipe.split_column(projectID,usercolumn,userSeparator,remove_original_column=usersetremove)
                                    # something special here
                                    # if split into several columns, then usercolumn will change
                                elif userOperates==8:
                                    if Confirm("Are you sure to stop doing Data Wrangling?",default=False):
                                        break
                    elif userMode==3:
                        if Confirm("Exit and transfer to another column operations",default=False):
                            break
                print(GetColumnName(projectID))
                usercolumn=raw_input("Continue Enter the column name, if no other steps, Enter N: ")
        elif choice==5:
            if Confirm("Are you sure to exit?",default=False):
                with open('HybridWF.json','wt')as f:
                    json.dump(result,f,indent=2)
                break




if __name__=='__main__':
    main()


# // extendend Or  execution











