
import json


inputdatalist=[]

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

userinputpath=checkpath()


with open(userinputpath,'r')as f:
    data=json.load(f)
    for dicts in data:
        # print('@begin '+dicts['op']+'@desc '+dicts['description']+'\n')
        if dicts['op']=='core/column-rename':
            # print('@in '+dicts['oldColumnName']+'\n')
            # print('@in '+dicts['newColumnName']+'\n')
            oldColumnName='oldColumnName:'+dicts['oldColumnName']
            newColumnName='newColumnName:'+dicts['newColumnName']
            inputdatalist.append(oldColumnName)
            inputdatalist.append(newColumnName)

        elif dicts['op']=='core/mass-edit':
            colname='col-name:'+dicts['columnName']
            try:
                cluster_function='cluster-function:'+dicts['Cluster-function']
                cluster_type='cluster-type:'+dicts['Cluster-type']
                cluster_params='cluster-params:'+dicts['Cluster-params']
                inputdatalist.append(colname)
                inputdatalist.append(cluster_function)
                inputdatalist.append(cluster_params)
                inputdatalist.append(cluster_type)
            except KeyError:
                cluster_edits='Edits:'+str(dicts['edits'])
                inputdatalist.append(cluster_edits)
        elif dicts['op']=='core/text-transform':
            colname='col-name:'+dicts['columnName']
            expression='expression:'+dicts['expression']
            inputdatalist.append(colname)
            inputdatalist.append(expression)
        elif dicts['op']=='core/column-split':
            colname='col-name:'+dicts['columnName']
            separator='separator:'+'"%s"'%(dicts['separator'])
            inputdatalist.append(colname)
            inputdatalist.append(separator)


deinputdatalist=set(inputdatalist)

# for sublist in list(deinputdatalist):
#     print('@in '+sublist)

# for the subset of the procedure

# parse and print it out
f=open('BCLinearParseYW.txt','w')
f.write('@begin LinearBCOR@desc Workflow of Extended openrefine history\n')
for sublist in list(deinputdatalist):
    f.write('@param '+sublist+'\n')
f.write('@in dtable0\n')
f.write('@out dtable%d\n'%(len(data)-1))
rename_c=0
massedit_c=0
texttrans_c=0
colsplit_c=0
table_c=0
for dicts in data:
    if dicts['op']=='core/column-rename':
        f.write('@begin core/column-rename%d'%rename_c+'@desc '+dicts['description']+'\n')
        f.write('@param oldColumnName:'+dicts['oldColumnName']+'\n')
        f.write('@param newColumnName:'+dicts['newColumnName']+'\n')
        f.write('@in dtable%d\n'%table_c)
        table_c+=1
        f.write('@out dtable%d\n'%table_c)
        f.write('@end core/column-rename%d\n'%rename_c)

        rename_c+=1

    elif dicts['op']=='core/mass-edit':
        f.write('@begin core/mass-edit%d'%massedit_c+'@desc '+dicts['description']+'\n')
        f.write('@param col-name:'+dicts['columnName']+'\n')
        try:
            f.write('@param cluster-type:%s\n'%dicts['Cluster-type'])
            f.write('@param cluster-params:%s\n'%dicts['Cluster-params'])
            f.write('@param cluster-function:%s\n'%dicts['Cluster-function'])
        except KeyError:
            f.write('@param Edits:%s\n'%str(dicts['edits']))
        f.write('@in dtable%d\n'%table_c)
        table_c+=1
        f.write('@out dtable%d\n'%table_c)
        f.write('@end core/mass-edit%d\n'%massedit_c)
        massedit_c+=1
    elif dicts['op']=='core/text-transform':
        f.write('@begin core/text-transform%d'%texttrans_c+'@desc '+dicts['description']+'\n')
        f.write('@param col-name:'+dicts['columnName']+'\n')
        f.write('@param expression:'+dicts['expression']+'\n')
        f.write('@in dtable%d\n'%table_c)
        table_c+=1
        f.write('@out dtable%d\n'%table_c)
        f.write('@end core/text-transform%d\n'%texttrans_c)
        texttrans_c+=1
    elif dicts['op']=='core/column-split':
        f.write('@begin core/column-split%d'%colsplit_c+'@desc '+dicts['description']+'\n')
        f.write('@param col-name:'+dicts['columnName']+'\n')
        f.write('@param separator:'+'"%s"'%(dicts['separator'])+'\n')
        f.write('@in dtable%d\n'%table_c)
        table_c+=1
        f.write('@out dtable%d\n'%table_c)
        f.write('@end core/column-split%d\n'%colsplit_c)
        colsplit_c+=1


f.write('@end LinearBCOR\n')
f.close()
