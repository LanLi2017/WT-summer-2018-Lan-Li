import json
from itertools import groupby
from pprint import pprint

with open('userScript.json','r')as f:
    data=json.load(f)
    # first part rename and output dtable
    rename_c=0
    for dicts in data:
        if dicts['op']=='core/column-rename':
            rename_c+=1
    # sort the left to parallel the operations
    data[rename_c:]=sorted(data[rename_c:],key=lambda k:k['columnName'])

# groupby the columnName
list_of_lists=[]
newdata=data[rename_c:]
for key,group in groupby(newdata,lambda x:x['columnName'].split()[0]):
    list_of_lists.append(list(group))
# pprint(list_of_lists)

splitlists=[]
# separate Split schema operation
for innerlists in list_of_lists:
    for innerdicts in innerlists:
        if innerdicts['op']=='core/column-split':
           splitlists.append(innerlists)

# substraction of the list of lists of dicts
newlist_of_lists=[item for item in list_of_lists if item not in splitlists]

# print all of the #@in
inputdatalist=[]
for dicts in data:
    # print('#@begin '+dicts['op']+'#@desc '+dicts['description']+'\n')
    if dicts['op']=='core/column-rename':
        # print('#@in '+dicts['oldColumnName']+'\n')
        # print('#@in '+dicts['newColumnName']+'\n')
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
        remove='removeOriginalColumn:%s'%dicts['removeOriginalColumn']
        inputdatalist.append(colname)
        inputdatalist.append(separator)
        inputdatalist.append(remove)
deinputdatalist=set(inputdatalist)


# count how many steps for schema level
table_counter=0
# rename operations and split operations
for dicts in data:
    if dicts['op']=='core/column-rename' or dicts['op']=='core/column-split':
        table_counter+=1

outtable=table_counter+1



# parse into YW model
f=open('../yw/2Original_SPParseYW.txt','w')
f.write('#@begin SPOriginalOR2#@desc Workflow of Linear original openrefine history\n')
for sublist in list(deinputdatalist):
    f.write('#@param '+sublist+'\n')
f.write('#@in table0\n')
f.write('#@out table%d\n'%outtable)
table_c=0
i=0
# rename operations
for dicts in data[:rename_c]:
    if dicts['op']=='core/column-rename':
        f.write('#@begin core/column-rename%d'%i+'#@desc '+dicts['description']+'\n')
        f.write('#@param oldColumnName:'+dicts['oldColumnName']+'\n')
        f.write('#@param newColumnName:'+dicts['newColumnName']+'\n')
        f.write('#@in table%d\n'%table_c)
        table_c+=1
        f.write('#@out table%d\n'%table_c)
        f.write('#@end core/column-rename%d\n'%i)
        i+=1

#operations on column (column level)
# schema level
def ruleforreturn(ind,tc,colname,table_counter):

    # [{'columnName':Sponsor, 'function':value.toNumber()},{....}]
    # [{'columnName':event, 'function':value.toDate()},{.....}]
    if ind==0:
       f.write('#@in table%d\n'%table_counter)
       f.write('#@out %s%d\n'%(colname,tc))
    else:
        f.write('#@in %s%d\n'%(colname,tc-1))
        f.write('#@out %s%d\n'%(colname,tc))



# Schema level (Rename, Split)



massedit_c=0
texttrans_c=0

for lists in newlist_of_lists:
    count=0
    tc=1
    for dicts in lists:
        col_name='col:%s'%dicts['columnName']
        if dicts['op']=='core/mass-edit':
            f.write('#@begin core/mass-edit%d'%massedit_c+'#@desc '+dicts['description']+'\n')
            f.write('#@param col-name:'+dicts['columnName']+'\n')
            ruleforreturn(count,tc,col_name,table_c)
            tc+=1
            count+=1
            f.write('#@end core/mass-edit%d\n'%massedit_c)
            massedit_c+=1
        elif dicts['op']=='core/text-transform':
            f.write('#@begin core/text-transform%d'%texttrans_c+'#@desc '+dicts['description']+'\n')
            f.write('#@param col-name:'+dicts['columnName']+'\n')
            f.write('#@param expression:'+dicts['expression']+'\n')
            ruleforreturn(count,tc,col_name,table_c)
            tc+=1
            count+=1
            f.write('#@end core/text-transform%d\n'%texttrans_c)
            texttrans_c+=1

    # f.write('#@end OperationsOn%s\n'%list_of_sublists[a][0])
colsplit_c=0
dtable_c=table_c



def ruleforsplitreturn(ind,opname,tablecounter,columnName,columnCounter,splitlit):
    if ind==0 and opname=='core/column-split':
        f.write('#@in table%d\n'%tablecounter)
        tablecounter+=1
        f.write('#@out table%d\n'%tablecounter)
    if ind==0 and opname!='core/column-split':
        f.write('#@in table%d\n'%tablecounter)
        columnCounter+=1
        f.write('#@out %s%d\n'%(columnName,columnCounter))
    if ind!=0 and opname=='core/column-split':
        f.write('#@in %s%d\n'%(columnName,columnCounter))
        tablecounter+=1
        f.write('#@out table%d\n'%tablecounter)
    if ind!=0 and opname!='core/column-split':
        f.write('#@in %s%d\n'%(columnName,columnCounter))
        columnCounter+=1
        f.write('#@out %s%d\n'%(columnName,columnCounter))


for splitlist in splitlists:
    indexsplit=0
    col_counter=0
    for splitdicts in splitlist:
        splitcol=splitdicts['columnName'].split()
        opname=splitdicts['op']
        col_namesplit='col:%s'%splitdicts['columnName']
        if opname=='core/column-split':
            f.write('#@begin core/column-split%d'%colsplit_c+'#@desc %s\n'%(splitdicts['description'])+'\n')
            f.write('#@param separator:"%s"\n'%(splitdicts['separator']))
            f.write('#@param removeOriginalColumn:%s\n'%splitdicts['removeOriginalColumn'])
            f.write('#@param col-name:%s\n'%splitdicts['columnName'])
            ruleforsplitreturn(indexsplit,opname,dtable_c,col_namesplit,col_counter,splitlist)
            indexsplit+=1
            dtable_c+=1
            # f.write('#@in table%d\n'%table_c)
            # dtable_c+=1
            # f.write('#@out table%d\n'%dtable_c)
            f.write('#@end core/column-split%d\n'%colsplit_c)
            colsplit_c+=1
        elif opname=='core/mass-edit':
            f.write('#@begin core/mass-edit%d'%massedit_c+'#@desc '+splitdicts['description']+'\n')
            f.write('#@param col-name:"%s"\n'%splitdicts['columnName'])
            ruleforsplitreturn(indexsplit,opname,dtable_c,col_namesplit,col_counter,splitlist)
            indexsplit+=1
            col_counter+=1
            print(col_counter)
            f.write('#@end core/mass-edit%d\n'%massedit_c)
            massedit_c+=1
        elif opname=='core/text-transform':
            f.write('#@begin core/text-transform%d'%texttrans_c+'#@desc '+splitdicts['description']+'\n')
            f.write('#@param col-name:'+splitdicts['columnName']+'\n')
            f.write('#@param expression:'+splitdicts['expression']+'\n')
            ruleforsplitreturn(indexsplit,opname,dtable_c,col_namesplit,col_counter,splitlist)
            indexsplit+=1
            col_counter+=1
            print(col_counter)
            f.write('#@end core/text-transform%d\n'%texttrans_c)
            texttrans_c+=1


f.write('#@begin MergeOperationsColumns #@desc Merge the Parallel Column operations\n')
for a in range(len(newlist_of_lists)):
    newcol_name='col:%s'%(newlist_of_lists[a][0]['columnName'])
    colcounter=len(newlist_of_lists[a])
    f.write('#@in %s%d\n'%(newcol_name,colcounter))


for b in range(len(splitlists)):
    lenthdicts=len(splitlists[b])
    if splitlists[b][lenthdicts-1]['op']=='core/column-split':
        f.write('#@in table%d\n'%dtable_c)
    else:
        col_c=lenthdicts-1
        f.write('#@in %s%d\n'%(splitlists[b][0]['columnName'],col_c))

outtable=dtable_c+1
f.write('#@out table%d\n'%outtable)
f.write('#@end MergeOperationsColumns\n')

f.write('#@end SPOriginalOR2\n')
f.close()
