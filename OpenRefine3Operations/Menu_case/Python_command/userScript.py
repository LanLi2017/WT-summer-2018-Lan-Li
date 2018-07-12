import csv

import OpenRefinerecipe
from OpenRefine3Operations.Menu_case.Python_command.google import refine


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


def main():
    print("Welcome to use OpenRefine userScript")
    print("raw_input your services choice")
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
        elif choice==4:
            usergetprojectID=raw_input("input the project ID:")
            OpenRefinerecipe.get_project_name(usergetprojectID)
        elif choice==2:
            userinputpath=raw_input("input the file path:")
            userinputName=raw_input("input the project Name:")
            projectID=OpenRefinerecipe.create_project(userinputpath,userinputName)
            number_rows=raw_input("Display some number of rows: You can choose 5/10/25/50")
            print("Show the first "+number_rows+" rows for this project:")

            with open(userinputpath,'rb') as project:
                content=tuple(project)
                header=content[0]
                print(header)
                # data=tuple(content[1:int(number_rows)+1])
                for i in range(1,int(number_rows)+1):
                    print(content[i])

            userrenamechoice=raw_input("Enter the column name you want to change, if there is no choice , please enter N: ")
            while userrenamechoice!='N':
                newcolumnname=raw_input("Enter the new column name:")
                OpenRefinerecipe.rename_column(projectID,userrenamechoice,newcolumnname)
                userrenamechoice=raw_input("Continue Enter the column name you want to change, if there is no choice, please Enter N: ")

            # split row mode and record mode
            response=OpenRefinerecipe.get_models(projectID)
            column_model = response['columnModel']
            column_name = [column['name'] for column in column_model['columns']]
            print(column_name)
            usercolumn=raw_input("Enter the column name you want to do Data Wrangling,if there is no other columns you want to make change, enter N: ")
            while usercolumn!='N':
                while True:
                    userMode=prompt_options([
                        'row mode',
                        'record mode',
                        'Exit',
                    ])
                    if userMode==2:
                        # five steps
                        # 1. identify the field that contains the records marker
                        userStandardColumn=raw_input("Please input the records marker: ")
                        # 2. move this field as the first column
                        OpenRefinerecipe.reorder_columns(projectID,0)
                        # 3. sort this column (no corresponding function)
                    elif userMode==1:

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
                                if userOperates==1:
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
                                            print(compute_clusters)
                                            userClusterinput=raw_input("Do you want to do manually edition for cluster? If not, input N; else input Y: ")
                                            Edit_from=OpenRefinerecipe.getFromValue(compute_clusters)
                                            Edit_to=OpenRefinerecipe.getToValue(compute_clusters)
                                            if userClusterinput =='N':
                                                edits=[{'from':f, 'to':t} for f,t in zip(Edit_from, Edit_to)]
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
                                                mannually_edits=[{'from':f, 'to':t} for f,t in zip(Edit_from, Edit_new_to)]
                                                OpenRefinerecipe.mass_edit(projectID,usercolumn,mannually_edits,expression='value')

                                elif userOperates==2:
                                    OpenRefinerecipe.text_transform(projectID,usercolumn,'value.trim()')
                                elif userOperates==3:
                                    OpenRefinerecipe.text_transform(projectID,usercolumn,'value.toLowercase()')
                                elif userOperates==4:
                                    OpenRefinerecipe.text_transform(projectID,usercolumn,'value.toUppercase()')
                                elif userOperates==5:
                                    OpenRefinerecipe.text_transform(projectID,usercolumn,'value.toDate()')
                                elif userOperates==6:
                                    OpenRefinerecipe.text_transform(projectID,usercolumn,'value.toNumber()')
                                elif userOperates==7:
                                    userSeparator=raw_input("input the separator: ")
                                    OpenRefinerecipe.split_column(projectID,usercolumn,userSeparator)
                                elif userOperates==8:
                                    if Confirm("Are you sure to stop doing Data Wrangling?",default=False):
                                        break
                    elif userMode==3:
                        if Confirm("Are you sure to exit?",default=False):
                            break
                usercolumn=raw_input("Continue Enter the column name, if no other steps, Enter N: ")
        elif choice==5:
            if Confirm("Are you sure to exit?",default=False):
                break




if __name__=='__main__':
    main()














