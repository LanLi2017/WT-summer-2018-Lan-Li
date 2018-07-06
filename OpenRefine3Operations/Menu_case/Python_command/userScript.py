import csv

import OpenRefinerecipe
from OpenRefine3Operations.Menu_case.Python_command.google import refine

print("Welcome to use OpenRefine userScript")
print("raw_input your services choice")
print("1.List projects")
print("2.Create project")
print("3.Open project")
print("4.Get Project Name")
# import project
userChoice=raw_input("Enter a number:")
print(type(userChoice))
if userChoice=='1':
    OpenRefinerecipe.list_objects()
elif userChoice=='3':
    userinputID=raw_input("input the project ID:")
    OpenRefinerecipe.open_project(userinputID)
elif userChoice=='4':
    usergetprojectID=raw_input("input the project ID:")
    OpenRefinerecipe.get_project_name(usergetprojectID)
elif userChoice=='2':
    userinputpath=raw_input("input the file path:")
    userinputName=raw_input("input the project Name:")
    projectID=OpenRefinerecipe.create_project(userinputpath,userinputName)
    number_rows=raw_input("number of rows: You can choose 5/10/25/50")
    print("Show the first "+number_rows+" rows for this project:")

    with open(userinputpath,'rb') as project:
        content=tuple(project)
        header=content[0]
        data=tuple(content[1:])
        for i in range(int(number_rows)):
            print content[i]
    # response=OpenRefinerecipe.get_models(projectID)
    # column_model = response['columnModel']
    # column_name = [column['name'] for column in column_model['columns']]
    # print(column_name)
    userrenamechoice=raw_input("Enter the column name you want to change, if there is no choice , please enter N: ")
    while userrenamechoice!='N':
        newcolumnname=raw_input("Enter the new column name:")
        OpenRefinerecipe.rename_column(projectID,userrenamechoice,newcolumnname)
        userrenamechoice=raw_input("Continue Enter the column name you want to change, if there is no choice, please Enter N: ")


    usercolumn=raw_input("Enter the column name you want to do Data Wrangling: ")
    print("1. mass edit")
    userOperates=raw_input("Enter a number:")

    if userOperates=='1':
        print("please choose clusterer type:")
        print("1. binning")
        print("2. knn")
        userClusterer=raw_input("Enter the number:")
        if userClusterer=='1':
            print("please choose function:")
            print("1. fingerprint")
            userFunction=raw_input("Enter the number:")
            if userFunction=='1':
                params=raw_input("Enter the params:")
                compute_clusters=OpenRefinerecipe.compute_clusters(projectID,usercolumn,clusterer_type='binning',function='ngram-fingerprint',params=params)
                Edit_from=OpenRefinerecipe.getFromValue(compute_clusters)
                Edit_to=OpenRefinerecipe.getToValue(compute_clusters)
                edits=[{'from':f, 'to':t} for f,t in zip(Edit_from, Edit_to)]
                OpenRefinerecipe.mass_edit(projectID,usercolumn,edits,expression='value')






