#!/usr/bin/env bash
# @begin PyOpenRefineCommand @desc Using python command to do Openrefine data wrangling
# @in csvFile @uri file: partTest.csv
# @in refinePythonFile @uri file: refine.py
# @in column_name
# @in newColumnName
# @in oldColumnName
# @in expression1 @as trimMethod
# @in expression2 @as lowercaseMethod
# @in clusterer_type @as method
# @in function @as keying_function
# @in params @as Ngram_size
# @out Json_History_time
# @out Json_History_id
# @out Json_History_description
# @out Json_History_code
# @out outputFile @uri file:PartTest.tsv


# @begin CreateProject @desc create project from file
# @in csvFile
# @in refinePythonFile @uri file: refine.py
# @out projectID
# @out projectNoRows
python refine.py --create partTest.csv
# @end CreateProject

python -i refine.py
#
#import StringIO
from google.refine import refine

# @begin RenameColumn
# @in projectID
# @in column @as oldColumnName
# @in new_column @as newColumnName
# @out table1
refine.RefineProject(refine.RefineServer(),'2293580976387').rename_column('sponsor','sponsorName')
# @end RenameColumn


# @begin TrimWhitespace @desc Invoke text_transform function and replace the expression with trim method
# @in table1
# @in projectID
# @in column_name
# @in trimMethod
# @out table2
refine.RefineProject(refine.RefineServer(),'2293580976387').text_transform('sponsor','value.trim()')
# @end TrimWhitespace


# @begin LowercaseColumn @desc Invoke text_transform functiona nd replace the expression with lowercase method
# @in table2
# @in projectID
# @in column_name
# @in lowercaseMethod
# @out table3
refine.RefineProject(refine.RefineServer(),'2293580976387').text_transform('sponsor','value.toLowercase()')
# @end LowercaseColumn


# @begin ComputeClusters @desc Returns a list of clusters of {'value':...,'count':...}
# @in table3
# @in projectID
# @in column_name
# @in method
# @in keying_function
# @in Ngram_size
# @out count @as No_Facet_Name
# @out value @as Facet_Name
# @out table3
refine.RefineProject(refine.RefineServer(),'2293580976387').compute_clusters('sponsor',clusterer_type='binning',function='ngram-fingerprint', params=20)
# @end ComputeClusters

# @begin Edit&Cluster @desc Invoke mass_edit function and using the list of clusters from previous step to replace the edits: from and to
# @in table3
# @in projectID
# @in No_Facet_Name
# @in Facet_Name
# @in column_name
# @out Json_History_time
# @out Json_History_id
# @out Json_History_description
# @out Json_History_code
# @out table4
refine.RefineProject(refine.RefineServer(),'2293580976387').mass_edit('sponsor',[{'from': ['norddeutscher lloyd bremen','norddeutscher lloyd  bremen'], 'to': 'norddeutscher lloyd bremen'}])
# @end Edit&Cluster

# export project
# @begin exportProject @desc Export the project
# @in table4
# @in Json_History_id
# @out outputFile @uri file: PartTest.tsv
python refine.py --export 1952314595639 --output=PartTest.tsv
# @end exportProject


# @end PyOpenRefineCommand
