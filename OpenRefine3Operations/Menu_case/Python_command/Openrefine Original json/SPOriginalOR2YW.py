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
print('@begin SPOriginalOR@desc Workflow of Linear original openrefine history\n')
for sublist in list(deinputdatalist):
    print('@in '+sublist)
print('@in dtable0\n')
print('@out dtable-cleaned\n')
table_c=0
i=0
# rename operations
for dicts in data[:rename_c]:
    if dicts['op']=='core/column-rename':
        print('@begin core/column-rename%d'%i+'@desc '+dicts['description']+'\n')
        print('@in oldColumnName:'+dicts['oldColumnName']+'\n')
        print('@in newColumnName:'+dicts['newColumnName']+'\n')
        print('@in dtable%d\n'%table_c)
        table_c+=1
        print('@out dtable%d\n'%table_c)
        print('@end core/column-rename%d\n'%i)
        i+=1

#operations on column
#inner operations

massedit_c=0
texttrans_c=0
colsplit_c=0


def ruleforreturn(list1,ind):
    i=len(list1)
    # [{'columnName':Sponsor, 'function':value.toNumber()},{....}]
    # [{'columnName':event, 'function':value.toDate()},{.....}]
    indexi=0
    if i==1:
        print('@in dtable%d\n'%table_c)
        print('@out dtable%s\n'%(list1[ind]['columnName']))
    else:
        if ind==0:
           print('@in dtable%d\n'%table_c)
           print('@out dt0')
        if ind in range(1,i-1):
            print('@in dt%d\n'%indexi)
            indexi+=1
            print('@out dt%d\n'%indexi)
        if ind==i-1:
            print('@in dt%d\n'%indexi)
            print('@out dtable%s\n'%(list1[ind]['columnName']))


# list_of_sublists
# [[colname:Sponsor, value.totrim(),value.toLowercase()],[],....]
# list of lists
# [[{'columnname':sponsor},{}], [{'columnname':call_number}]]
for a in range(len(list_of_sublists)):
    print('@begin OperationsOn%s'%list_of_sublists[a][0]+'@desc Serial column operations on Column %s\n'%list_of_lists[a][0]['columnName'])
    for subnewlists in list_of_sublists[a]:
        print('@in %s\n'%subnewlists)
    print('@in dtable%d\n'%table_c)
    print('@out dtable%s\n'%list_of_lists[a][0]['columnName'])
    count=0
    for b in range(len(list_of_lists[a])):
        if list_of_lists[a][b]['op']=='core/mass-edit':
            print('@begin core/mass-edit%d'%massedit_c+'@desc '+list_of_lists[a][b]['description']+'\n')
            print('@in col-name:'+list_of_lists[a][b]['columnName']+'\n')
            ruleforreturn(list_of_lists[a],count)
            count+=1
            print('@end core/mass-edit%d'%massedit_c)
            massedit_c+=1
        elif list_of_lists[a][b]['op']=='core/text-transform':
            print('@begin core/text-transform%d'%texttrans_c+'@desc '+list_of_lists[a][b]['description']+'\n')
            print('@in col-name:'+list_of_lists[a][b]['columnName']+'\n')
            print('@in expression:'+list_of_lists[a][b]['expression']+'\n')
            ruleforreturn(list_of_lists[a],count)
            count+=1
            print('@end core/text-transform%d\n'%texttrans_c)
            texttrans_c+=1
        elif list_of_lists[a][b]['op']=='core/column-split':
            print('@begin core/column-split%d'%colsplit_c+'@desc '+list_of_lists[a][b]['description']+'\n')
            print('@in col-name:'+list_of_lists[a][b]['columnName']+'\n')
            print('@in separator:'+'"%s"\n'%(list_of_lists[a][b]['separator']))
            ruleforreturn(list_of_lists[a],count)
            count+=1
            print('@end core/column-split%d\n'%colsplit_c)
            colsplit_c+=1

    print('@end OperationsOn%s\n'%list_of_sublists[a][0])

print('@begin MergeOperationsColumns @desc Merge the Parallel Column operations\n')
for c in range(len(list_of_lists)):
    print('@in dtable%s\n'%list_of_lists[c][0]['columnName'])
print('@out dtable-cleaned\n')
print('@end MergeOperationsColumns\n')

print('@end SPOriginalOR\n')
