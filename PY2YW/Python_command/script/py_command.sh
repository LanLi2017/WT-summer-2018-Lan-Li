#!/usr/bin/env bash
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
# @out outputFile @uri file: PartTest.tsv
# @out projectID
# @out projectNoRows


# @begin CreateProject @desc create project from file
# @in csvFile @uri file: partTest.csv
# @in refinePythonFile @uri file: refine.py
# @out projectID
# @out projectNoRows
python refine.py --create partTest.csv
# @end CreateProject

python -i refine.py

from StringIO import StringIO


# @begin RenameColumn @desc Rename column name to make original table more meaningful
# @in projectID
# @in oldColumnName
# @in newColumnName
# @out table1
refine.RefineProject(refine.RefineServer(),'2146520884101').rename_column('Column','ColumnTag')
# @end RenameColumn


# @begin OperationsColSponsor @desc OpenRefine operations on column sponsor
# @in table1
# @in projectID
# @in columnName:"sponsor"
# @in expression:"value.trim()"
# @in expression:"value.toLowercase()"
# @in clusterer_type:"binning"
# @in function:"ngram-fingerprint"
# @in params:"20"
# @in to:'norddeutscher lloyd bremen'
# @out table1-Sponsor

# @begin TrimWhitespaceColSponsor @desc Invoke text_transform function and replace the expression with trim method
# @in projectID
# @in table1
# @in expression:"value.trim()"
# @in columnName:"sponsor"
# @out t2
refine.RefineProject(refine.RefineServer(),'2146520884101').text_transform('sponsor','value.trim()')
# @end TrimWhitespaceColSponsor

# @begin LowercaseColSponsor @desc Invoke text_transform function and replace the exprssion with lowercase method
# @in projectID
# @in t2
# @in expression:"value.toLowercase()"
# @in columnName:"sponsor"
# @out t3
refine.RefineProject(refine.RefineServer(),'2146520884101').text_transform('sponsor','value.toLowercase()')
# @end LowercaseColSponsor

# @begin EditCells&ClusterColSponsor @desc Mass edit cells in column sponsor
# @in projectID
# @in t3
# @in columnName:"sponsor"
# @in clusterer_type:"binning"
# @in function:"ngram-fingerprint"
# @in params:"20"
# @in to:'norddeutscher lloyd bremen'
# @out table1-Sponsor

# @begin ComputeClusterColSponsor @desc Using cluster method and function to do clustering
# @in projectID
# @in t3
# @in columnName:"sponsor"
# @in clusterer_type:"binning"
# @in function:"ngram-fingerprint"
# @in params:"20"
# @out from:['norddeutscher lloyd bremen','norddeutscher lloyd  bremen']
# @out t4
refine.RefineProject(refine.RefineServer(),'2146520884101').compute_clusters('sponsor',clusterer_type='binning',function='ngram-fingerprint', params=20)
# @end ComputeClusterColSponsor

# @begin MassEditColSponsor @desc Using clusters with mass edit
# @in projectID
# @in t4
# @in columnName:"sponsor"
# @in from:['norddeutscher lloyd bremen','norddeutscher lloyd  bremen']
# @in to:'norddeutscher lloyd bremen'
# @out table1-Sponsor
refine.RefineProject(refine.RefineServer(),'2146520884101').mass_edit('sponsor',[{'from': ['norddeutscher lloyd bremen','norddeutscher lloyd  bremen'], 'to': 'norddeutscher lloyd bremen'}])
# @end MassEditColSponsor


# @end EditCells&ClusterColSponsor

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
# @out table1-Event

# @begin EditCells&ClusterColEvent @desc Mass edit cells in column event
# @in projectID
# @in table1
# @in columnName:"event"
# @in clusterer_type:"knn"
# @in function:"PPM"
# @in params:{'radius':1,'blocking-ngram-size':6}
# @in to:'THANKSGIVING DINNER'
# @out t6

# @begin ComputeClusterColEvent @desc Using cluster method and function to do clustering
# @in projectID
# @in table1
# @in columnName:"event"
# @in clusterer_type:"knn"
# @in function:"PPM"
# @in params:{'radius':1,'blocking-ngram-size':6}
# @out from:['THANKSGIVING DINNER','THANKSGIVING DAY DINNER']
# @out t5
refine.RefineProject(refine.RefineServer(),'2146520884101').compute_clusters('event',clusterer_type='knn',function='PPM', params={ 'radius':1,'blocking-ngram-size':6})
# @end ComputeClusterColEvent

# @begin MassEditColEvent @desc Using clusters with mass edit
# @in to:'THANKSGIVING DINNER'
# @in projectID
# @in columnName:"event"
# @in t5
# @in from:['THANKSGIVING DINNER','THANKSGIVING DAY DINNER']
# @out t6
refine.RefineProject(refine.RefineServer(),'2146520884101').mass_edit('event',[{'from':['THANKSGIVING DINNER','THANKSGIVING DAY DINNER'],'to':'THANKSGIVING DINNER'}])
# @end MassEditColEvent

# @end EditCells&ClusterEvent

# @begin LowercaseColEvent @desc Invoke text_transform function and replace the expression with lowercase method
# @in projectID
# @in t6
# @in expression:"value.toLowercase()"
# @in columnName:"event"
# @out t7
refine.RefineProject(refine.RefineServer(),'2146520884101').text_transform('event','value.toLowercase()')
# @end LowercaseColEvent

# @begin TrimWhitespaceColEvent @desc Invoke text_transform function and replace the expression with trim method
# @in projectID
# @in t7
# @in expression:"value.trim()"
# @in columnName:"event"
# @out table1-Event
refine.RefineProject(refine.RefineServer(),'2146520884101').text_transform('event','value.trim()')
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
refine.RefineProject(refine.RefineServer(), '2146520884101').split_column('call_number', separator='-', mode='separator')
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
refine.RefineProject(refine.RefineServer(), '2146520884101').text_transform('dish_count', 'value.toNumber()')
# @end ToNumberColDish_count

# @end OperationsColDish_count


# @begin OperationsColPlace @desc OpenRefine functions on column place
# @in projectID
# @in table1
# @in columnName:"place"
# @in clusterer_type:"knn"
# @in function:"levenshtein"
# @in to:['Waldorf Astoria','Hamburg Amerika Linie','Norddeutscher Lloyd Bremen']
# @out table1-Place

# @begin EditCells&ClusterColPlace @desc Mass edit cells in column place
# @in projectID
# @in table1
# @in columnName:"place"
# @in clusterer_type:"knn"
# @in function:"levenshtein"
# @in to:['Waldorf Astoria','Hamburg Amerika Linie','Norddeutscher Lloyd Bremen']
# @out table1-Place


# @begin ComputeClusterColPlace @desc Using cluster method and function to do clustering
# @in projectID
# @in table1
# @in columnName:"place"
# @in clusterer_type:"knn"
# @in function:"levenshtein"
# @out from:{['Waldorf Astoria','Waldorf-Astoria'],['Hamburg Amerika Line','Hamburg Amerika Linie'],['Norddeutscher Lloyd Bremen','Norddeutscher Lloyd  Bremen']}
# @out t8

refine.RefineProject(refine.RefineServer(),'2146520884101').compute_clusters('place',clusterer_type='knn',function='levenshtein')
#[[{'count': 4, 'value': u'Waldorf Astoria'}, {'count': 1, 'value': u'Waldorf-Astoria'}], [{'count': 1, 'value': u'Hamburg Amerika Line'}, {'count': 1, 'value': u'Hamburg Amerika Linie'}], [{'count': 5, 'value': u'Norddeutscher Lloyd Bremen'}, {'count': 2, 'value': u'Norddeutscher Lloyd  Bremen'}]]
# @end ComputeClusterColPlace

# @begin MassEditColPlace @desc Using clusters with mass edit
# @in projectID
# @in t8
# @in columnName:"place"
# @in from:{['Waldorf Astoria','Waldorf-Astoria'],['Hamburg Amerika Line','Hamburg Amerika Linie'],['Norddeutscher Lloyd Bremen','Norddeutscher Lloyd  Bremen']}
# @in to:['Waldorf Astoria','Hamburg Amerika Linie','Norddeutscher Lloyd Bremen']
# @out table1-Place
refine.RefineProject(refine.RefineServer(),'2146520884101').mass_edit('place',[{'from':['Waldorf Astoria','Waldorf-Astoria'],'to':'Waldorf Astoria'},{'from':['Hamburg Amerika Line','Hamburg Amerika Linie'],'to':'Hamburg Amerika Line'},{'from':['Norddeutscher Lloyd Bremen','Norddeutscher Lloyd  Bremen'],'to':'Norddeutscher Lloyd Bremen'}])
# @end MassEditColPlace

# @end EditCells&ClusterColPlace
# @end OperationsColPlace

# @begin exportProject @desc Export the project
# @in table1-Sponsor
# @in table1-Call_number
# @in table1-Event
# @in table1-Dish_count
# @in table1-Place
# @in Json_History_id
# @out outputFile @uri file: PartTest.tsv
python refine.py --export 2146520884101 --output=PartTest.tsv

# @end export project

# @end Parallel&SequentialModel
