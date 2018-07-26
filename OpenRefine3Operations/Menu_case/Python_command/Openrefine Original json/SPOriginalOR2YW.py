import json
from itertools import groupby
from operator import itemgetter

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
for key,group in groupby(newdata,lambda x:x['columnName']):
    list_of_lists.append(list(group))


#
# with open('newJson.json','w')as f:
#     f.writelines(json.dumps(data,indent=2))

# print all of the @in
inputdatalist=[]
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

# inner sub-in for every columnName subworkflow
subinputlists=[]
subinnerlist=[]
# [[{sponsor1,sponsor2,sponsor3}],[event1,event2,event3],[call_number1,call_number2],....]
#[[sponsor_in],[event_in],[call_number_in],....]
for subprelist in list_of_lists:
    for subinpredicts in subprelist:
        if subinpredicts['op']=='core/mass-edit':
            colname='col-name:'+subinpredicts['columnName']
            subinnerlist.append(colname)
        elif subinpredicts['op']=='core/text-transform':
            colname='col-name:'+subinpredicts['columnName']
            expression='expression:'+subinpredicts['expression']
            subinnerlist.append(colname)
            subinnerlist.append(expression)
        elif subinpredicts['op']=='core/column-split':
            colname='col-name:'+subinpredicts['columnName']
            separator='separator:'+'"%s"'%(subinpredicts['separator'])
            subinnerlist.append(colname)
            subinnerlist.append(separator)
        subinputlists.append(subinnerlist)
        subinnerlist=[]

# inner inputs list of list [[],[],...]
list_of_sublists=[
    [k] +[item[1]for item in g]
    for k,g in groupby(subinputlists,itemgetter(0))
]




# parse
f=open('Original_SPParseYW.txt','w')
f.write('@begin SPOriginalOR@desc Workflow of Linear original openrefine history\n')
for sublist in list(deinputdatalist):
    f.write('@in '+sublist+'\n')
f.write('@in dtable0\n')
f.write('@out dtable-cleaned\n')
table_c=0
i=0
# rename operations
for dicts in data[:rename_c]:
    if dicts['op']=='core/column-rename':
        f.write('@begin core/column-rename%d'%i+'@desc '+dicts['description']+'\n')
        f.write('@in oldColumnName:'+dicts['oldColumnName']+'\n')
        f.write('@in newColumnName:'+dicts['newColumnName']+'\n')
        f.write('@in dtable%d\n'%table_c)
        table_c+=1
        f.write('@out dtable%d\n'%table_c)
        f.write('@end core/column-rename%d\n'%i)
        i+=1

#operations on column
#inner operations

massedit_c=0
texttrans_c=0
colsplit_c=0


def ruleforreturn(list1,ind,tc):
    i=len(list1)
    # [{'columnName':Sponsor, 'function':value.toNumber()},{....}]
    # [{'columnName':event, 'function':value.toDate()},{.....}]
    if i==1:
        f.write('@in dtable%d\n'%table_c)
        f.write('@out dtable%s\n'%(list1[ind]['columnName']))
    else:
        # for ind in range(i):
        #     if ind==0:
        #         f.write('@in dtable%d\n'%table_c)
        #         f.write('@out dt0\n')
        #     elif ind==i-1:
        #         f.write('@in dt%d\n'%indexi)
        #         f.write('@out dtable%s\n'%(list1[ind]['columnName']))
        #     else:
        #         f.write('@in dt%d\n'%indexi)
        #         indexi+=1
        #         f.write('@out dt%d\n'%indexi)

        if ind==0:
           f.write('@in dtable%d\n'%table_c)
           f.write('@out dt%d\n'%tc)
        if ind in range(1,i-1):
            f.write('@in dt%d\n'%(tc-1))
            f.write('@out dt%d\n'%tc)
        if ind==i-1:
            f.write('@in dt%d\n'%(tc-1))
            f.write('@out dtable%s\n'%(list1[ind]['columnName']))


# list_of_sublists
# [[colname:Sponsor, value.totrim(),value.toLowercase()],[],....]
# list of lists
# [[{'columnname':sponsor},{}], [{'columnname':call_number}]]
for a in range(len(list_of_sublists)):
    f.write('@begin OperationsOn%s'%list_of_sublists[a][0]+'@desc Serial column operations on Column %s\n'%list_of_lists[a][0]['columnName'])
    for subnewlists in list_of_sublists[a]:
        f.write('@in %s\n'%subnewlists)
    f.write('@in dtable%d\n'%table_c)
    f.write('@out dtable%s\n'%list_of_lists[a][0]['columnName'])
    count=0
    tc=0
    for b in range(len(list_of_lists[a])):
        if list_of_lists[a][b]['op']=='core/mass-edit':
            f.write('@begin core/mass-edit%d'%massedit_c+'@desc '+list_of_lists[a][b]['description']+'\n')
            f.write('@in col-name:'+list_of_lists[a][b]['columnName']+'\n')
            ruleforreturn(list_of_lists[a],count,tc)
            tc+=1
            count+=1
            f.write('@end core/mass-edit%d'%massedit_c)
            massedit_c+=1
        elif list_of_lists[a][b]['op']=='core/text-transform':
            f.write('@begin core/text-transform%d'%texttrans_c+'@desc '+list_of_lists[a][b]['description']+'\n')
            f.write('@in col-name:'+list_of_lists[a][b]['columnName']+'\n')
            f.write('@in expression:'+list_of_lists[a][b]['expression']+'\n')
            ruleforreturn(list_of_lists[a],count,tc)
            tc+=1
            count+=1
            f.write('@end core/text-transform%d\n'%texttrans_c)
            texttrans_c+=1
        elif list_of_lists[a][b]['op']=='core/column-split':
            f.write('@begin core/column-split%d'%colsplit_c+'@desc '+list_of_lists[a][b]['description']+'\n')
            f.write('@in col-name:'+list_of_lists[a][b]['columnName']+'\n')
            f.write('@in separator:'+'"%s"\n'%(list_of_lists[a][b]['separator']))
            ruleforreturn(list_of_lists[a],count,tc)
            tc+=1
            count+=1
            f.write('@end core/column-split%d\n'%colsplit_c)
            colsplit_c+=1

    f.write('@end OperationsOn%s\n'%list_of_sublists[a][0])

f.write('@begin MergeOperationsColumns @desc Merge the Parallel Column operations\n')
for c in range(len(list_of_lists)):
    f.write('@in dtable%s\n'%list_of_lists[c][0]['columnName'])
f.write('@out dtable-cleaned\n')
f.write('@end MergeOperationsColumns\n')

f.write('@end SPOriginalOR\n')
f.close()
