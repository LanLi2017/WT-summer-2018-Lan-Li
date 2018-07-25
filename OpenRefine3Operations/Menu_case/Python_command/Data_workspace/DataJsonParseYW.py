
import json


inputdatalist=[]


with open('Datajsonformal.json','r')as f:
    data=json.load(f)
    outputfinal='dtable'+str(len(data))
    for dicts in data:
        try:
            # print('@begin '+dicts['op']+'@desc '+dicts['description']+'\n')
            if dicts['operation']['op']=='core/column-rename':
                # print('@in '+dicts['oldColumnName']+'\n')
                # print('@in '+dicts['newColumnName']+'\n')
                oldColumnName='oldColumnName:'+dicts['operation']['oldColumnName']
                newColumnName='newColumnName:'+dicts['operation']['newColumnName']
                inputdatalist.append(oldColumnName)
                inputdatalist.append(newColumnName)

            elif dicts['operation']['op']=='core/mass-edit':
                colname='col-name:'+dicts['operation']['columnName']
                inputdatalist.append(colname)
            elif dicts['operation']['op']=='core/text-transform':
                colname='col-name:'+dicts['operation']['columnName']
                expression='expression:'+dicts['operation']['expression']
                inputdatalist.append(colname)
                inputdatalist.append(expression)
            elif dicts['operation']['op']=='core/column-split':
                colname='col-name:'+dicts['operation']['columnName']
                separator='separator:'+'"%s"'%(dicts['operation']['separator'])
                inputdatalist.append(colname)
                inputdatalist.append(separator)
        except KeyError:
            pass



deinputdatalist=set(inputdatalist)

# for sublist in list(deinputdatalist):
#     print('@in '+sublist)

# for the subset of the procedure

# parse and print it out
f=open('LinearDataJsonParseYW.txt','w')
f.write('@begin LinearDataORJson@desc Workflow of Linear original openrefine history from data directory\n')
for sublist in list(deinputdatalist):
    f.write('@in '+sublist+'\n')
f.write('@in dtable0\n')
f.write('@out '+outputfinal+'\n')
rename_c=0
massedit_c=0
texttrans_c=0
colsplit_c=0
table_c=0
for dicts in data:
    try:
        if dicts['operation']['op']=='core/column-rename':
            f.write('@begin core/column-rename%d'%rename_c+'@desc '+dicts['description']+'\n')
            f.write('@in oldColumnName:'+dicts['operation']['oldColumnName']+'\n')
            f.write('@in newColumnName:'+dicts['operation']['newColumnName']+'\n')
            f.write('@in dtable%d\n'%table_c)
            table_c+=1
            f.write('@out dtable%d\n'%table_c)
            f.write('@end core/column-rename%d\n'%rename_c)

            rename_c+=1

        elif dicts['operation']['op']=='core/mass-edit':
            f.write('@begin core/mass-edit%d'%massedit_c+'@desc '+dicts['description']+'\n')
            f.write('@in col-name:'+dicts['operation']['columnName']+'\n')
            f.write('@in dtable%d\n'%table_c)
            table_c+=1
            f.write('@out dtable%d\n'%table_c)
            f.write('@end core/mass-edit%d\n'%massedit_c)
            massedit_c+=1
        elif dicts['operation']['op']=='core/text-transform':
            f.write('@begin core/text-transform%d'%texttrans_c+'@desc '+dicts['description']+'\n')
            f.write('@in col-name:'+dicts['operation']['columnName']+'\n')
            f.write('@in expression:'+dicts['operation']['expression']+'\n')
            f.write('@in dtable%d\n'%table_c)
            table_c+=1
            f.write('@out dtable%d\n'%table_c)
            f.write('@end core/text-transform%d\n'%texttrans_c)
            texttrans_c+=1
        elif dicts['operation']['op']=='core/column-split':
            f.write('@begin core/column-split%d'%colsplit_c+'@desc '+dicts['description']+'\n')
            f.write('@in col-name:'+dicts['operation']['columnName']+'\n')
            f.write('@in separator:'+'"%s"'%(dicts['operation']['separator'])+'\n')
            f.write('@in dtable%d\n'%table_c)
            table_c+=1
            f.write('@out dtable%d\n'%table_c)
            f.write('@end core/column-split%d\n'%colsplit_c)
            colsplit_c+=1
    except KeyError:
        f.write('@begin ManualEdit'+'@desc %s\n'%dicts['description'])
        f.write('@in dtable%d\n'%table_c)
        table_c+=1
        f.write('@out dtable%d\n'%table_c)
        f.write('@end ManualEdit\n')


f.write('@end LinearDataORJson\n')
f.close()
