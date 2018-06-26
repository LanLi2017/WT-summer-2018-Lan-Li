# def getValue(list1):
#     chosenvalue=[]
#     for listex in list1:
#         chosendic=listex[0]
#         for dic in listex:
#             if dic['count']>=chosendic['count']:
#                 chosendic=dic
#                 chosenvalue.append(chosendic['value'])
#     print(chosenvalue)




def getValue(computeCluster):
    result=[
        max(list_of_dicts, key=lambda d: d['count'])
        for list_of_dicts in computeCluster
    ]
    chosenvaluelist=[]
    for chosendict in result:
        chosenvaluelist.append(chosendict['value'])
    print(chosenvaluelist)
    return chosenvaluelist



def main():
    list1=[
    [{'count': 4, 'value': u'Waldorf Astoria'}, {'count': 1, 'value': u'Waldorf-Astoria'}],
    [{'count': 1, 'value': u'HAMBURG-AMERIKA LINE'}, {'count': 1, 'value': u'HAMBURG-AMERIKA LINIE'}],
    [{'count': 4, 'value': u'NORDDEUTSCHER LLOYD BREMEN'}, {'count': 2, 'value': u'NORDDEUTSCHER LLOYD  BREMEN'}]
    ]

    # get to list
    result=[
        max(list_of_dicts, key=lambda d: d['count'])
        for list_of_dicts in list1
    ]
    chosenvaluelist=[]
    for chosendict in result:
        chosenvaluelist.append(chosendict['value'])
    print(chosenvaluelist)

    # get from list
    fromlist=[]
    fromlist1=[]
    for list3 in list1:
        for list4 in list3:
            fromlist1.append(list4['value'])
        fromlist.append(fromlist1)
        fromlist1=[]
    print(fromlist)


    print('=====================================')
    # combine them
    c=[{'from':f, 'to': t} for f,t in zip(fromlist,chosenvaluelist)]
    print(c)
if __name__=='__main__':
    main()
