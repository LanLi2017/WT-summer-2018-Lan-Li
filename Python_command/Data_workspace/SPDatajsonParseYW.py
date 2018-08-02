import json
from itertools import groupby
from operator import itemgetter

import itertools

with open('Datajsonformal.json','r')as f:
    data=json.load(f)
    # first part rename and output dtable
    rename_c=0
    for dicts in data:
        try:
            if dicts['operation']['op']=='core/column-rename':
                rename_c+=1
                # sort the left to parallel the operations
                data[rename_c:]=sorted(data[rename_c:],key=lambda k:k['operation']['columnName'])
        except KeyError:
            pass

# groupby the columnName
list_of_lists=[]
newdata=data[rename_c:]
list_of_Manual=[]

try:
    for key,group in groupby(newdata,lambda x:x['operation']['columnName']):
        list_of_lists.append(list(group))
except KeyError:
    pass



#
# with open('newJson.json','w')as f:
#     f.writelines(json.dumps(data,indent=2))
ManualEdit_columnName=[]

# print all of the @in
inputdatalist=[]
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
        ManualEditin=dicts['description'].split()
        colname='col-name:'+ManualEditin[len(ManualEditin)-1]
        inputdatalist.append(colname)
        ManualEdit_columnName.append(ManualEditin[len(ManualEditin)-1])

        # ManualEditdesclist=ManualEditdesc.split()
print(ManualEdit_columnName)
deinputdatalist=set(inputdatalist)
print("hello world")
print(deinputdatalist)

# inner sub-in for every columnName subworkflow
subinputlists=[]
subinnerlist=[]

ManualEditdesc=[]

# [[{sponsor1,sponsor2,sponsor3}],[event1,event2,event3],[call_number1,call_number2],....]
#[[sponsor_in],[event_in],[call_number_in],....]
for subprelist in list_of_lists:
    for subinpredicts in subprelist:
        try:
            if subinpredicts['operation']['op']=='core/mass-edit':
                colname='col-name:'+subinpredicts['operation']['columnName']
                subinnerlist.append(colname)
            elif subinpredicts['operation']['op']=='core/text-transform':
                colname='col-name:'+subinpredicts['operation']['columnName']
                expression='expression:'+subinpredicts['operation']['expression']
                subinnerlist.append(colname)
                subinnerlist.append(expression)
            elif subinpredicts['operation']['op']=='core/column-split':
                colname='col-name:'+subinpredicts['operation']['columnName']
                separator='separator:'+'"%s"'%(subinpredicts['operation']['separator'])
                subinnerlist.append(colname)
                subinnerlist.append(separator)
            subinputlists.append(subinnerlist)
            subinnerlist=[]
        except KeyError:
            ManualEditdesc.append(subinpredicts['description'])
            # colname='col-name:'+ManualEditin[len(ManualEditin)-1]
            # subinputlists.append(colname)


# inner inputs list of list [[],[],...]
print(subinputlists)
list_of_sublists=[
    [k] + list(itertools.chain(*list(item[1:] for item in g)))
    for k,g in groupby(subinputlists,itemgetter(0))
]




# parse
f=open('SPParseDataJsonYW.txt','w')
f.write('@begin SPDataOR2YW@desc Workflow of Linear original openrefine history\n')
for sublist in list(deinputdatalist):
    f.write('@param '+sublist+'\n')
f.write('@in dtable0\n')
f.write('@out dtable-cleaned\n')
table_c=0
i=0
# rename operations
for dicts in data[:rename_c]:
    if dicts['operation']['op']=='core/column-rename':
        f.write('@begin core/column-rename%d'%i+'@desc '+dicts['operation']['description']+'\n')
        f.write('@param oldColumnName:'+dicts['operation']['oldColumnName']+'\n')
        f.write('@param newColumnName:'+dicts['operation']['newColumnName']+'\n')
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
        f.write('@out dtable%s\n'%(list1[ind]['operation']['columnName']))
    else:
        if ind==0:
           f.write('@in dtable%d\n'%table_c)
           f.write('@out dt0\n')
        if ind in range(1,i-1):
            f.write('@in dt%d\n'%(tc-1))
            f.write('@out dt%d\n'%tc)
        if ind==i-1:
            f.write('@in dt%d\n'%(tc-1))
            f.write('@out dtable%s\n'%(list1[ind]['operation']['columnName']))


# list_of_sublists
# [[colname:Sponsor, value.totrim(),value.toLowercase()],[],....]
# list of lists
# [[{'columnname':sponsor},{}], [{'columnname':call_number}]]
for a in range(len(list_of_sublists)):
    f.write('@begin OperationsOn%s'%list_of_sublists[a][0]+'@desc Serial column operations on Column %s\n'%list_of_lists[a][0]['operation']['columnName'])
    for subnewlists in list_of_sublists[a]:
        f.write('@param %s\n'%subnewlists)
    f.write('@in dtable%d\n'%table_c)
    f.write('@out dtable%s\n'%list_of_lists[a][0]['operation']['columnName'])
    count=0
    tc=0
    for b in range(len(list_of_lists[a])):
        if list_of_lists[a][b]['operation']['op']=='core/mass-edit':
            f.write('@begin core/mass-edit%d'%massedit_c+'@desc '+list_of_lists[a][b]['description']+'\n')
            f.write('@param col-name:'+list_of_lists[a][b]['operation']['columnName']+'\n')
            ruleforreturn(list_of_lists[a],count,tc)
            tc+=1
            count+=1
            f.write('@end core/mass-edit%d'%massedit_c)
            massedit_c+=1
        elif list_of_lists[a][b]['operation']['op']=='core/text-transform':
            f.write('@begin core/text-transform%d'%texttrans_c+'@desc '+list_of_lists[a][b]['description']+'\n')
            f.write('@param col-name:'+list_of_lists[a][b]['operation']['columnName']+'\n')
            f.write('@param expression:'+list_of_lists[a][b]['operation']['expression']+'\n')
            ruleforreturn(list_of_lists[a],count,tc)
            tc+=1
            count+=1
            f.write('@end core/text-transform%d\n'%texttrans_c)
            texttrans_c+=1
        elif list_of_lists[a][b]['operation']['op']=='core/column-split':
            f.write('@begin core/column-split%d'%colsplit_c+'@desc '+list_of_lists[a][b]['description']+'\n')
            f.write('@param col-name:'+list_of_lists[a][b]['operation']['columnName']+'\n')
            f.write('@param separator:'+'"%s"\n'%(list_of_lists[a][b]['operation']['separator']))
            ruleforreturn(list_of_lists[a],count,tc)
            tc+=1
            count+=1
            f.write('@end core/column-split%d\n'%colsplit_c)
            colsplit_c+=1

    f.write('@end OperationsOn%s\n'%list_of_sublists[a][0])

#  Manual Edit
f.write('@begin ManualEdit'+'@desc Manual Edit for cells\n')
for colNameManual in ManualEdit_columnName:
    f.write('@param col-name:%s\n'%colNameManual)


f.write('@out dtableManualEdit\n')
f.write('@end ManualEdit\n')

f.write('@begin MergeOperationsColumns @desc Merge the Parallel Column operations\n')
for c in range(len(list_of_lists)):
    f.write('@in dtable%s\n'%list_of_lists[c][0]['operation']['columnName'])
f.write('@in dtableManualEdit\n')
f.write('@out dtable-cleaned\n')
f.write('@end MergeOperationsColumns\n')

f.write('@end SPDataOR2YW\n')
f.close()
