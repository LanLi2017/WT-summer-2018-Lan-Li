# @begin Parallel&SequentialModel
# @in csvFile @uri file: partTest.csv
# @in refinePythonFile @uri file: refine.py
# @in oldColumnName
# @in newColumnName
# @in columnName:"sponsor"
# @in expression:"value.trim()"
# @in expression:"value.toLowercase()"
# @in clusterer_type:"binning"
# @in function:"ngram-fingerprint"
# @in params:"20"
# @in to:'norddeutscher lloyd bremen'
# @in columnName:"event"
# @in clusterer_type:"knn"
# @in function:"PPM"
# @in params:{'radius':1,'blocking-ngram-size':6}
# @in to:'THANKSGIVING DINNER'
# @in columnName:"call_number"
# @in separator:"-"
# @in mode:"separator"
# @in columnName:"dish_count"
# @in expression:"value.toNumber()"
# @in columnName:"place"
# @in function:"levenshtein"
# @in to:['Waldorf Astoria','Hamburg Amerika Linie','Norddeutscher Lloyd Bremen']
# @in Json_History_id
# @in function:getToValue
# @in function:getFromValue
# @out outputFile @uri file: PartTest.tsv
# @out projectID
# @out projectNoRows


# @begin CreateProject @desc create project from file
# @in csvFile @uri file: partTest.csv
# @in refinePythonFile @uri file: refine.py
# @out projectID
# @out projectNoRows
from google.refine import refine
projectID=refine.Refine(refine.RefineServer()).new_project('partTest.csv','HalfMenuDataset','.csv')[1]
# print(refine.myParser('--list'))
# @end CreateProject


'''insert a function to automatically get 'from' '''
def getFromValue(computeCluster):
    fromlist=[]
    fromlistInner=[]
    for list3 in computeCluster:
        for list4 in list3:
            fromlistInner.append(list4['value'])
        fromlist.append(fromlistInner)
        fromlistInner=[]
    return fromlist


'''insert a function to automatically get 'to' '''
def getToValue(computeCluster):
    result=[
        max(list_of_dicts, key=lambda d: d['count'])
        for list_of_dicts in computeCluster
    ]
    chosenvaluelist=[]
    for chosendict in result:
        chosenvaluelist.append(chosendict['value'])
    return chosenvaluelist

# @begin RenameColumn @desc Rename column name to make original table more meaningful
# @in projectID
# @in oldColumnName
# @in newColumnName
# @out table1
refine.RefineProject(refine.RefineServer(),projectID).rename_column('notes','commands')
# @end RenameColumn


# @begin OperationsColSponsor @desc OpenRefine operations on column sponsor
# @in table1
# @in projectID
# @in columnName:"sponsor"
# @in expression:"value.trim()"
# @in expression:"value.toLowercase()"
# @in clusterer_type:"binning"
# @in function:"ngram-fingerprint"
# @in function:getToValue
# @in function:getFromValue
# @in params:"20"
# @out table1-Sponsor

# @begin TrimWhitespaceColSponsor @desc Invoke text_transform function and replace the expression with trim method
# @in projectID
# @in table1
# @in expression:"value.trim()"
# @in columnName:"sponsor"
# @out t2
refine.RefineProject(refine.RefineServer(),projectID).text_transform('sponsor','value.trim()')
# @end TrimWhitespaceColSponsor

# @begin LowercaseColSponsor @desc Invoke text_transform function and replace the expression with lowercase method
# @in projectID
# @in t2
# @in expression:"value.toLowercase()"
# @in columnName:"sponsor"
# @out t3
refine.RefineProject(refine.RefineServer(),projectID).text_transform('sponsor','value.toLowercase()')
# @end LowercaseColSponsor

# @begin Cluster&EditCellsColSponsor @desc Mass edit cells in column sponsor
# @in projectID
# @in t3
# @in columnName:"sponsor"
# @in clusterer_type:"binning"
# @in function:"ngram-fingerprint"
# @in params:"20"
# @in function:getToValue
# @in function:getFromValue
# @out table1-Sponsor

# @begin ComputeClusterColSponsor @desc Using cluster method and function to do clustering
# @in projectID
# @in t3
# @in columnName:"sponsor"
# @in clusterer_type:"binning"
# @in function:"ngram-fingerprint"
# @in params:"20"
# @out t3withcluster
t3withcluster=refine.RefineProject(refine.RefineServer(),projectID).compute_clusters('sponsor',clusterer_type='binning',function='ngram-fingerprint', params=20)
# @end ComputeClusterColSponsor

# @begin ChooseUniqueName2MassEdit @desc Using Function getTovalue and getFromValue for edits, which is [{'from': ['foo'], 'to': 'bar'}, {...}]
# @in t3withcluster
# @in function:getToValue
# @in function:getFromValue
# @out EditsColSponsor
fromlistSponsor=getFromValue(t3withcluster)
tolistSponsor=getToValue(t3withcluster)
EditsColSponsor=[{'from':f, 'to':t} for f,t in zip(fromlistSponsor, tolistSponsor)]
# @end ChooseUniqueName2MassEdit

# @begin MassEditColSponsor @desc Using clusters with mass edit
# @in projectID
# @in t3withcluster
# @in columnName:"sponsor"
# @in EditsColSponsor
# @out table1-Sponsor
refine.RefineProject(refine.RefineServer(),projectID).mass_edit('sponsor',EditsColSponsor)
# @end MassEditColSponsor


# @end Cluster&EditCellsColSponsor

# @end OperationColSponsor



# @begin OperationsColEvent @desc OpenRefine operations on column event
# @in projectID
# @in table1
# @in columnName:"event"
# @in clusterer_type:"knn"
# @in function:"PPM"
# @in params:{'radius':1,'blocking-ngram-size':6}
# @in to:'THANKSGIVING DINNER'
# @in expression:"value.trim()"
# @in expression:"value.toLowercase()"
# @in function:getToValue
# @in function:getFromValue
# @out table1-Event

# @begin Cluster&EditCellsColEvent @desc Mass edit cells in column event
# @in projectID
# @in table1
# @in columnName:"event"
# @in clusterer_type:"knn"
# @in function:"PPM"
# @in params:{'radius':1,'blocking-ngram-size':6}
# @in function:getToValue
# @in function:getFromValue
# @out t6

# @begin ComputeClusterColEvent @desc Using cluster method and function to do clustering
# @in projectID
# @in table1
# @in columnName:"event"
# @in clusterer_type:"knn"
# @in function:"PPM"
# @in params:{'radius':1,'blocking-ngram-size':6}
# @out table1withclusterColEvent
table1withclusterColEvent=refine.RefineProject(refine.RefineServer(),projectID).compute_clusters('event',clusterer_type='knn',function='PPM', params={ 'radius':1,'blocking-ngram-size':6})
# @end ComputeClusterColEvent

# @begin ChooseUniqueName2MassEdit @desc Using Function getTovalue and getFromValue for edits, which is [{'from': ['foo'], 'to': 'bar'}, {...}]
# @in table1withclusterColEvent
# @in function:getToValue
# @in function:getFromValue
# @out EditsColEvent
fromlistEvent=getFromValue(table1withclusterColEvent)
tolistEvent=getToValue(table1withclusterColEvent)
EditsColEvent=[{'from':f, 'to':t} for f,t in zip(fromlistEvent, tolistEvent)]
# @end ChooseUniqueName2MassEdit

# @begin MassEditColEvent @desc Using clusters with mass edit
# @in projectID
# @in columnName:"event"
# @in EditsColEvent
# @in table1withclusterColEvent
# @out t6
refine.RefineProject(refine.RefineServer(),projectID).mass_edit('event',EditsColEvent)
# @end MassEditColEvent

# @end Cluster&EditCellsColEvent

# @begin LowercaseColEvent @desc Invoke text_transform function and replace the expression with lowercase method
# @in projectID
# @in t6
# @in expression:"value.toLowercase()"
# @in columnName:"event"
# @out t7
refine.RefineProject(refine.RefineServer(),projectID).text_transform('event','value.toLowercase()')
# @end LowercaseColEvent

# @begin TrimWhitespaceColEvent @desc Invoke text_transform function and replace the expression with trim method
# @in projectID
# @in t7
# @in expression:"value.trim()"
# @in columnName:"event"
# @out table1-Event
refine.RefineProject(refine.RefineServer(),projectID).text_transform('event','value.trim()')
# @end TrimWhitespaceColEvent

# @end OperationsColEvent

# @begin OperationsColCall_number @desc OpenRefine operations on column call_number
# @in table1
# @in projectID
# @in columnName:"call_number"
# @in separator:"-"
# @in mode:"separator"
# @out table1-Call_number

# @begin SplitCellsColCall_number @desc Split multi-valued cells in column call_number
# @in projectID
# @in table1
# @in columnName:"call_number"
# @in separator:"-"
# @in mode:"separator"
# @out table1-Call_number
refine.RefineProject(refine.RefineServer(), projectID).split_column('call_number', separator='-', mode='separator')
# @end SplitCellsColCall_number

# @end OperationsColCall_number

# @begin OperationsColDish_count @desc OpenRefine operations on column dish_count
# @in projectID
# @in table1
# @in columnName:"dish_count"
# @in expression:"value.toNumber()"
# @out table1-Dish_count

# @begin ToNumberColDish_count @desc Text transform on cells in column dish_count using expression value.toNumber()
# @in projectID
# @in table1
# @in columnName:"dish_count"
# @in expression:"value.toNumber()"
# @out table1-Dish_count
refine.RefineProject(refine.RefineServer(), projectID).text_transform('dish_count', 'value.toNumber()')
# @end ToNumberColDish_count

# @end OperationsColDish_count


# @begin OperationsColPlace @desc OpenRefine functions on column place
# @in projectID
# @in table1
# @in columnName:"place"
# @in clusterer_type:"knn"
# @in function:"levenshtein"
# @in function:getToValue
# @in function:getFromValue
# @out table1-Place

# @begin Cluster&EditCellsColPlace @desc Mass edit cells in column place
# @in projectID
# @in table1
# @in columnName:"place"
# @in clusterer_type:"knn"
# @in function:"levenshtein"
# @in function:getToValue
# @in function:getFromValue
# @out table1-Place


# @begin ComputeClusterColPlace @desc Using cluster method and function to do clustering
# @in projectID
# @in table1
# @in columnName:"place"
# @in clusterer_type:"knn"
# @in function:"levenshtein"
# @out table1withclusterColplace
table1withclusterColplace=refine.RefineProject(refine.RefineServer(),projectID).compute_clusters('place',clusterer_type='knn',function='levenshtein')
#[[{'count': 4, 'value': u'Waldorf Astoria'}, {'count': 1, 'value': u'Waldorf-Astoria'}], [{'count': 1, 'value': u'Hamburg Amerika Line'}, {'count': 1, 'value': u'Hamburg Amerika Linie'}], [{'count': 5, 'value': u'Norddeutscher Lloyd Bremen'}, {'count': 2, 'value': u'Norddeutscher Lloyd  Bremen'}]]
# @end ComputeClusterColPlace

# @begin ChooseUniqueName2MassEdit @desc Using Function getTovalue and getFromValue for edits, which is [{'from': ['foo'], 'to': 'bar'}, {...}]
# @in table1withclusterColplace
# @in function:getToValue
# @in function:getFromValue
# @out EditsColPlace
fromlistPlace=getFromValue(table1withclusterColplace)
tolistPlace=getToValue(table1withclusterColplace)
EditsColPlace=[{'from':f, 'to':t} for f,t in zip(fromlistPlace, tolistPlace)]
# @end ChooseUniqueName2MassEdit


# @begin MassEditColPlace @desc Using clusters with mass edit
# @in projectID
# @in table1withclusterColplace
# @in columnName:"place"
# @in EditsColPlace
# @out table1-Place
refine.RefineProject(refine.RefineServer(),projectID).mass_edit('place', EditsColPlace)
# @end MassEditColPlace

# @end Cluster&EditCellsColPlace
# @end OperationsColPlace

# @begin MergeColumns @desc merge all columns after operations
# @in table1-Sponsor
# @in table1-Call_number
# @in table1-Event
# @in table1-Dish_count
# @in table1-Place
# @out newTable1

# @end MergeColumns


# @begin exportProject @desc Export the project
# @in newTable1
# @in Json_History_id
# @out outputFile @uri file: PartTest.tsv
refine.RefineProject(refine.RefineServer(),projectID).export('tsv')
# @end export project

# @end Parallel&SequentialModel

