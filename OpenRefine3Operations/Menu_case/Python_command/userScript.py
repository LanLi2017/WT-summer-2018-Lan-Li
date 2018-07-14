import csv

import OpenRefinerecipe
from OpenRefine3Operations.Menu_case.Python_command.google import refine

import subprocess

cmd = ['ls', '-l']

with open('output.txt', 'w') as out:
    return_code = subprocess.call(cmd, stdout=out)


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


def main():
    f=open('logWorkflow.json','w') # open file with name of 'logWorkflow.txt'
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
            # f.write('Open Project\n')
        elif choice==4:
            usergetprojectID=raw_input("input the project ID:")
            OpenRefinerecipe.get_project_name(usergetprojectID)
            # f.write('Get Project Name\n')
        elif choice==2:
            # f.write('Create Project\n')
            userinputpath=raw_input("input the file path:")
            userinputName=raw_input("input the project Name:")
            # f.write('@IN file path: %s\n'%userinputpath)
            # f.write('@IN project Name: %s\n'%userinputName)
            projectID=OpenRefinerecipe.create_project(userinputpath,userinputName)
            # f.write('@OUT New Project ID : %s\n'%projectID)

            number_rows=raw_input("Display some number of rows: You can choose 5/10/25/50")
            print("Show the first "+number_rows+" rows for this project:")

            with open(userinputpath,'rb') as project:
                content=tuple(project)
                header=content[0]
                print(header)
                # data=tuple(content[1:int(number_rows)+1])
                for i in range(1,int(number_rows)+1):
                    print(content[i])

            f.write('[\n')
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
                f.write('{\n')
                f.write('"op": "core/column-rename",\n')
                newcolumnname=raw_input("Enter the new column name:")
                f.write('"description": "Rename column %s to %s",\n'%(userrenamechoice, newcolumnname))
                f.write('"oldColumnName": "%s",\n'%userrenamechoice)
                f.write('"newColumnName": "%s"\n'%newcolumnname)
                f.write('}\n')
                OpenRefinerecipe.rename_column(projectID,userrenamechoice,newcolumnname)
                userrenamechoice=raw_input("Continue Enter the column name you want to change, if there is no choice, please Enter N: ")

            # split row mode and record mode
            print(GetColumnName(projectID))
            usercolumn=raw_input("Enter the column name you want to do Data Wrangling,if there is no other columns you want to make change, enter N: ")
            while usercolumn!='N':
                # f.write('Data Wrangling On Column %s\n'%usercolumn)
                while True:
                    userMode=prompt_options([
                        'row mode',
                        'record mode',
                        'Exit',
                    ])
                    if userMode==2:
                        # f.write('Record mode \n')
                        # five steps
                        # 1. identify the field that contains the records marker
                        userStandardColumn=raw_input("Please input the records marker: ")
                        # 2. move this field as the first column
                        OpenRefinerecipe.reorder_columns(projectID,0)
                        # 3. sort this column (no corresponding function)
                    elif userMode==1:

                            # f.write('Row mode \n')
                            while True:
                                userOperates=prompt_options([
                                    'Mass Edit',
                                    'Trim Whitespace',
                                    'Lowercase the column value',
                                    'Uppercase the column value',
                                    'Transform the column value to Date',
                                    'Transform the column value to Numeric',
                                    'Split multi-valued cells in column ',
                                    'Exit',
                                ])
                                if userOperates !=8:
                                    f.write(',\n')
                                else:
                                    f.write('\n')
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

                                    f.write('{\n')
                                    f.write('"op": "core/mass-edit",\n')
                                    f.write('"description:": "Mass edit cells in column %s ",\n'%usercolumn)
                                    f.write('"engineConfig": {"mode": "row-based","facets": []},\n')
                                    f.write('"columnName": "%s",\n'%usercolumn)
                                    f.write('"expression": "value",\n')
                                    f.write('"edits":[')
                                    print("please choose clusterer type:")
                                    print("1. binning")
                                    print("2. knn")
                                    userClusterer=raw_input("Enter the number:")
                                    if userClusterer=='1':
                                        userFunction=prompt_options([
                                            'fingerprint',
                                            'metaphone3',
                                            'cologne-phonetic',
                                        ])
                                        if userFunction==1:
                                            # f.write('"function": "fingerprint",\n')
                                            params=raw_input("Enter the params:")
                                            # f.write('"params": %s\n'%params)
                                            # f.write('}\n')
                                            print(type(f))
                                            compute_clusters=OpenRefinerecipe.compute_clusters(projectID,usercolumn,clusterer_type='binning',function='ngram-fingerprint',params=params)
                                        elif userFunction==2:
                                            # f.write('"function": "metaphone3"\n')
                                            # f.write('}\n')
                                            compute_clusters=OpenRefinerecipe.compute_clusters(projectID,usercolumn,clusterer_type='binning',function='metaphone3')
                                        elif userFunction==3:
                                            # f.write('"function": "cologne-phonetic"\n')
                                            # f.write('}\n')
                                            compute_clusters=OpenRefinerecipe.compute_clusters(projectID,usercolumn,clusterer_type='binning',function='cologne-phonetic')

                                    elif userClusterer=='2':
                                        # f.write('"type": "knn",\n')
                                        userKNNfunction=prompt_options([
                                           'levenshtein',
                                           'PPM',
                                        ])
                                        if userKNNfunction==1:
                                            # f.write('"function": "levenshtein",\n')
                                            print("Please set the params: ")
                                            userinputradius=float(raw_input("Set the radius: "))
                                            userinputNgramsize=int(raw_input("Set the Bloking Ngram-size: "))
                                            # f.write('"params": {"radius":%f, "blocking-ngram-size":%d}\n'%(userinputradius,userinputNgramsize))
                                            # f.write('}\n')
                                            compute_clusters=OpenRefinerecipe.compute_clusters(projectID,usercolumn,clusterer_type='knn',function='levenshtein',params={ 'radius':userinputradius,'blocking-ngram-size':userinputNgramsize})
                                        elif userKNNfunction==2:
                                            # f.write('"function": "PPM",\n')
                                            print("Please set the params: ")
                                            userinputradius=float(raw_input("Set the radius: "))
                                            userinputNgramsize=int(raw_input("Set the Bloking Ngram-size: "))
                                            # f.write('"params": {"radius":%f, "blocking-ngram-size":%d}\n'%(userinputradius,userinputNgramsize))
                                            # f.write('}\n')
                                            compute_clusters=OpenRefinerecipe.compute_clusters(projectID,usercolumn,clusterer_type='knn',function='PPM',params={ 'radius':userinputradius,'blocking-ngram-size':userinputNgramsize})
                                    print(compute_clusters)
                                    userClusterinput=raw_input("Do you want to do manually edition for cluster? If not, input N; else input Y: ")

                                    Edit_from=OpenRefinerecipe.getFromValue(compute_clusters)
                                    Edit_to=OpenRefinerecipe.getToValue(compute_clusters)
                                    ''' slice '''
                                    preEdit_from=Edit_from[:-1]
                                    lastEdit_from=Edit_from[-1:]
                                    preEdit_to=Edit_to[:-1]
                                    lastEdit_to=Edit_to[-1:]
                                    if userClusterinput =='N':
                                        edits=[{'from':f1, 'to':t} for f1,t in zip(Edit_from, Edit_to)]
                                        for fromset,tset in zip(preEdit_from,preEdit_to):
                                            f.write('{\n')
                                            f.write('"fromBlank": false,\n')
                                            f.write('"fromError": false,\n')
                                            f.write('"from": [\n')
                                            for i in range(len(fromset)-1):
                                                f.write('"%s",\n'%fromset[i])
                                            f.write('"%s"'%fromset[len(fromset)-1])

                                            f.write('],\n')
                                            f.write('"to": "%s"\n'%tset)
                                            f.write('}\n')
                                            f.write(',')
                                        for fsub,tsub in zip(lastEdit_from,lastEdit_to):
                                            f.write('{\n')
                                            f.write('"fromBlank": false,\n')
                                            f.write('"fromError": false,\n')
                                            f.write('"from": [\n')
                                            for i in range(len(fsub)-1):
                                                    f.write('"%s",\n'%fsub[i])
                                            f.write('"%s"'%fsub[len(fsub)-1])
                                            f.write('],\n')
                                            f.write('"to": "%s"\n'%tsub)
                                            f.write('}\n')
                                        f.write(']\n')
                                        f.write('}\n')
                                        OpenRefinerecipe.mass_edit(projectID,usercolumn,edits,expression='value')
                                    elif userClusterinput=='Y':
                                        print("This is the original values in cluster: ")
                                        print(Edit_from)
                                        print("This is the values after the chosen cluster: ")
                                        print(Edit_to)
                                        Edit_new_to=[]
                                        for to in Edit_to:
                                            userinputTo=raw_input("Input the value you want to make change, if not, input N")
                                            if userinputTo!='N':
                                                to=userinputTo
                                                Edit_new_to.append(to)
                                            else:
                                                to=to
                                                Edit_new_to.append(to)
                                        print(Edit_new_to)
                                        preEdit_new_to=Edit_new_to[:-1]
                                        lastEdit_new_to=Edit_new_to[-1:]
                                        mannually_edits=[{'from':f1, 'to':t} for f1,t in zip(Edit_from, Edit_new_to)]
                                        for fromset,tset in zip(preEdit_from,preEdit_new_to):
                                            f.write('{\n')
                                            f.write('"fromBlank": false,\n')
                                            f.write('"fromError": false,\n')
                                            f.write('"from": [\n')
                                            for i in range(len(fromset)-1):
                                                f.write('"%s",\n'%fromset[i])
                                            f.write('"%s"'%fromset[len(fromset)-1])

                                            f.write('],\n')
                                            f.write('"to": "%s"\n'%tset)
                                            f.write('}\n')
                                            f.write(',')
                                        for fsub,tsub in zip(lastEdit_from,lastEdit_new_to):
                                            f.write('{\n')
                                            f.write('"fromBlank": false,\n')
                                            f.write('"fromError": false,\n')
                                            f.write('"from": [\n')
                                            for i in range(len(fsub)-1):
                                                    f.write('"%s",\n'%fsub[i])
                                            f.write('"%s"'%fsub[len(fsub)-1])
                                            f.write('],\n')
                                            f.write('"to": "%s"\n'%tsub)
                                            f.write('}\n')
                                        f.write(']\n')
                                        f.write('}\n')
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
                                    f.write('{\n')
                                    f.write('"op": "core/text-transform",\n')
                                    f.write('"description": "Text transform on cells in column %s using expression value.trim()",\n'%usercolumn)
                                    f.write('"engineConfig": {"mode": "row-based","facets": []},\n')
                                    f.write('"columnName": "%s",\n'%usercolumn)
                                    f.write('"expression": "value.trim()",\n')
                                    f.write('"onError": "set-to-blank",\n')
                                    f.write('"repeat": false,\n')
                                    f.write('"repeatCount": 10\n')
                                    f.write('}\n')
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

                                    f.write('{\n')
                                    f.write('"op": "core/text-transform",\n')
                                    f.write('"description": "Text transform on cells in column %s using expression value.toLowercase()",\n'%usercolumn)
                                    f.write('"engineConfig": {"mode": "row-based","facets": []},\n')
                                    f.write('"columnName": "%s",\n'%usercolumn)
                                    f.write('"expression": "value.toLowercase()",\n')
                                    f.write('"onError": "set-to-blank",\n')
                                    f.write('"repeat": false,\n')
                                    f.write('"repeatCount": 10\n')
                                    f.write('}\n')
                                    OpenRefinerecipe.text_transform(projectID,usercolumn,'value.toLowercase()')
                                elif userOperates==4:

                                    f.write('{\n')
                                    f.write('"op": "core/text-transform",\n')
                                    f.write('"description": "Text transform on cells in column %s using expression value.toUppercase()",\n'%usercolumn)
                                    f.write('"engineConfig": {"mode": "row-based","facets": []},\n')
                                    f.write('"columnName": "%s",\n'%usercolumn)
                                    f.write('"expression": "value.toUppercase()",\n')
                                    f.write('"onError": "set-to-blank",\n')
                                    f.write('"repeat": false,\n')
                                    f.write('"repeatCount": 10\n')
                                    f.write('}\n')
                                    OpenRefinerecipe.text_transform(projectID,usercolumn,'value.toUppercase()')
                                elif userOperates==5:
                                    f.write('{\n')
                                    f.write('"op": "core/text-transform",\n')
                                    f.write('"description": "Text transform on cells in column %s using expression value.toDate()",\n'%usercolumn)
                                    f.write('"engineConfig": {"mode": "row-based","facets": []},\n')
                                    f.write('"columnName": "%s",\n'%usercolumn)
                                    f.write('"expression": "value.toDate()",\n')
                                    f.write('"onError": "set-to-blank",\n')
                                    f.write('"repeat": false,\n')
                                    f.write('"repeatCount": 10\n')
                                    f.write('}\n')
                                    OpenRefinerecipe.text_transform(projectID,usercolumn,'value.toDate()')
                                elif userOperates==6:
                                    f.write('{\n')
                                    f.write('"op": "core/text-transform",\n')
                                    f.write('"description": "Text transform on cells in column %s using expression value.toNumber()",\n'%usercolumn)
                                    f.write('"engineConfig": {"mode": "row-based","facets": []},\n')
                                    f.write('"columnName": "%s",\n'%usercolumn)
                                    f.write('"expression": "value.toNumber()",\n')
                                    f.write('"onError": "set-to-blank",\n')
                                    f.write('"repeat": false,\n')
                                    f.write('"repeatCount": 10\n')
                                    f.write('}\n')
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
                                    f.write('{\n')
                                    f.write('"op": "core/column-split",\n')
                                    f.write('"description": "Split column %s by separator",\n'%usercolumn)
                                    f.write('"engineConfig": {"mode": "row-based","facets": []},\n')
                                    f.write('"columnName": "%s",\n'%usercolumn)
                                    f.write('"guessCellType": true,\n')
                                    f.write('"removeOriginalColumn": true,\n')
                                    f.write('"mode": "separator",\n')
                                    f.write('"separator": " ",\n')
                                    f.write('"regex": false,\n')
                                    f.write('"maxColumns": 0\n')
                                    f.write('}\n')
                                    userSeparator=raw_input("input the separator: ")
                                    OpenRefinerecipe.split_column(projectID,usercolumn,userSeparator)
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
            f.write(']\n')

            if Confirm("Are you sure to exit?",default=False):
                break




if __name__=='__main__':
    main()














