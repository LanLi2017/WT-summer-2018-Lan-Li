import json
from itertools import groupby
from operator import itemgetter

import itertools
from pprint import pprint

with open('ExtendedWF.json','r')as f:
    data=json.load(f)
    # first part rename and output dtable
    rename_c=1
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
        cluster_function='cluster-function:'+dicts['Cluster-function']
        cluster_type='cluster-type:'+dicts['Cluster-type']
        cluster_params='cluster-params:'+dicts['Cluster-params']
        inputdatalist.append(colname)
        inputdatalist.append(cluster_function)
        inputdatalist.append(cluster_type)
        inputdatalist.append(cluster_params)
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
i=0
# rename operations
for dicts in data[:rename_c]:
    if dicts['op']=='core/column-rename':
        table_counter+=1
# f.write('#@end OperationsOn%s\n'%list_of_sublists[a][0])
for splitlist in splitlists:
    for splitdicts in splitlist:
        splitcol=splitdicts['columnName'].split()
        if len(splitcol)==1:
            table_counter+=1
outtable=table_counter+1



# parse into YW model
f=open('../yw/2X_SPParseYW.txt','w')
f.write('#@begin SPXOR2#@desc Workflow of Linear original openrefine history\n')
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
    tc=0
    for dicts in lists:
        col_name='col:%s'%dicts['columnName']
        if dicts['op']=='core/mass-edit':
            f.write('#@begin core/mass-edit%d'%massedit_c+'#@desc '+dicts['description']+'\n')
            f.write('#@param col-name:'+dicts['columnName']+'\n')
            f.write('#@param cluster-type:'+dicts['Cluster-type']+'\n')
            f.write('#@param cluster-function:'+dicts['Cluster-function']+'\n')
            f.write('#@param cluster-params:'+dicts['Cluster-params']+'\n')
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
for splitlist in splitlists:
    splitc=0
    splitindex=0
    for splitdicts in splitlist:
        splitcol=splitdicts['columnName'].split()
        if len(splitcol)==1:
            f.write('#@begin core/column-split%d'%colsplit_c+'#@desc %s\n'%(splitdicts['description'])+'\n')
            f.write('#@param separator:"%s"\n'%(splitdicts['separator']))
            f.write('#@param removeOriginalColumn:%s\n'%splitdicts['removeOriginalColumn'])
            f.write('#@in %s\n'%splitdicts['columnName'])
            f.write('#@in table%d\n'%table_c)
            dtable_c+=1
            f.write('#@out table%d\n'%dtable_c)
            f.write('#@end core/column-split%d\n'%colsplit_c)
            colsplit_c+=1
        elif len(splitcol)>1:
            colformsplitname='col:%s'%(splitdicts['columnName'].split()[0])
            if splitdicts['op']=='core/mass-edit':
                f.write('#@begin core/mass-edit%d'%massedit_c+'#@desc '+splitdicts['description']+'\n')
                f.write('#@param col-name:"%s"\n'%splitdicts['columnName'])
                ruleforreturn(splitindex,splitc,colformsplitname,dtable_c)
                splitc+=1
                splitindex+=1
                f.write('#@end core/mass-edit%d\n'%massedit_c)
                massedit_c+=1
            elif splitdicts['op']=='core/text-transform':
                f.write('#@begin core/text-transform%d'%texttrans_c+'#@desc '+splitdicts['description']+'\n')
                f.write('#@param col-name:'+splitdicts['columnName']+'\n')
                f.write('#@param expression:'+splitdicts['expression']+'\n')
                ruleforreturn(splitindex,splitc,colformsplitname,dtable_c)
                splitc+=1
                splitindex+=1
                f.write('#@end core/text-transform%d\n'%texttrans_c)
                texttrans_c+=1


f.write('#@begin MergeOperationsColumns #@desc Merge the Parallel Column operations\n')
for a in range(len(newlist_of_lists)):
    newcol_name='col:%s'%(newlist_of_lists[a][0]['columnName'])
    colcounter=len(newlist_of_lists[a])-1
    f.write('#@in %s%d\n'%(newcol_name,colcounter))


for b in range(len(splitlists)):
    if len(splitlists[b])==1:
        f.write('#@in table%d'%dtable_c)
    elif len(splitlists[b])>1:
        splitcol_name='col:%s'%(splitlists[b][0]['columnName'])
        splitcounter=len(splitlists[b])-2
        f.write('#@in %s%d\n'%(splitcol_name,splitcounter))
outtable=dtable_c+1
f.write('#@out table%d\n'%outtable)
f.write('#@end MergeOperationsColumns\n')

f.write('#@end SPXOR2\n')
f.close()
