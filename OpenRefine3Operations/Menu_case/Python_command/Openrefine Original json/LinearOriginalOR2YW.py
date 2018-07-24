
import json


inputdatalist=[]


with open('userScript.json','r')as f:
    data=json.load(f)
    outputfinal='dtable'+str(len(data))
    print(outputfinal)
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
            inputdatalist.append(colname)
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
print('@begin LinearOriginalOR@desc Workflow of Linear original openrefine history\n')
for sublist in list(deinputdatalist):
    print('@in '+sublist+'\n')
print('@in dtable0\n')
print('@out '+outputfinal+'\n')
rename_c=0
massedit_c=0
texttrans_c=0
colsplit_c=0
table_c=0
for dicts in data:
    if dicts['op']=='core/column-rename':
        print('@begin core/column-rename%d'%rename_c+'@desc '+dicts['description']+'\n')
        print('@in oldColumnName:'+dicts['oldColumnName']+'\n')
        print('@in newColumnName:'+dicts['newColumnName']+'\n')
        print('@in dtable%d'%table_c)
        table_c+=1
        print('@out dtable%d'%table_c)
        print('@end core/column-rename%d'%rename_c)

        rename_c+=1

    elif dicts['op']=='core/mass-edit':
        print('@begin core/mass-edit%d'%massedit_c+'@desc '+dicts['description']+'\n')
        print('@in col-name:'+dicts['columnName']+'\n')
        print('@in dtable%d'%table_c)
        table_c+=1
        print('@out dtable%d'%table_c)
        print('@end core/mass-edit%d'%massedit_c)
        massedit_c+=1
    elif dicts['op']=='core/text-transform':
        print('@begin core/text-transform%d'%texttrans_c+'@desc '+dicts['description']+'\n')
        print('@in col-name:'+dicts['columnName']+'\n')
        print('@in expression:'+dicts['expression']+'\n')
        print('@in dtable%d'%table_c)
        table_c+=1
        print('@out dtable%d'%table_c)
        print('@end core/text-transform%d'%texttrans_c)
        texttrans_c+=1
    elif dicts['op']=='core/column-split':
        print('@begin core/column-split%d'%colsplit_c+'@desc '+dicts['description']+'\n')
        print('@in col-name:'+dicts['columnName']+'\n')
        print('@in separator:'+'"%s"'%(dicts['separator']))
        print('@in dtable%d'%table_c)
        table_c+=1
        print('@out dtable%d'%table_c)
        print('@end core/column-split%d'%colsplit_c)
        colsplit_c+=1


print('@end LinearOriginalOR')
