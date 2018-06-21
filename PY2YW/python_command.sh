#!/usr/bin/env bash
# usage
# list all of the projects
python refine.py --list
# create project from file
python refine.py --create filepath.csv/tsv/..[FILE]
# apply rules from json file
python refine.py --apply filepath.json projectID/projectNAME
# export project to file
python refine.py --export projectID/projectNAME --output=filepath.tsv
# templating export
python refine.py --export "My Address Book" --template='{ "friend" : {{jsonize(cells["friend"].value)}}, "address" : {{jsonize(cells["address"].value)}} }' --prefix='{ "address" : [' --rowSeparator ',' --suffix '] }' --filterQuery="^mary$"
# show project metadata
python refine.py --info projectID/projectNAME
# delete project
python refine.py --delete projectID/projectNAME
# check usage
python refine.py --help

# functions
python -i refine.py
# show version of OpenRefine server
refine.RefineServer().get_version()
# show total rows of project
refine.RefineProject(refine.RefineServer(), projectID).do_json('get-rows')['total']
# get rows
refine.RefineProject(refine.RefineServer(), projectID).get_rows(facets=None, sort_by=None, start=0, limit=0)
# reorder_rows
refine.RefineProject(refine.RefineServer(), projectID).reorder_rows(sort_by=None)
# remove rows
refine.RefineProject(refine.RefineServer(), projectID).remove_rows(facets=None)
# text transform : using different expression to do the function
# Edit cells-> common transforms -> Trim leading and trailing whitespace
refine.RefineProject(refine.RefineServer(), projectID).text_transform(columnName, 'value.trim()',on_error='set-to-blank',repeat=False, repeat_count=10)
# Edit cells-> common transforms -> to titlecase
refine.RefineProject(refine.RefineServer(), projectID).text_transform(columnName, 'value.toTitlecase()',on_error='set-to-blank',repeat=False, repeat_count=10)
# Edit cells-> common transforms -> to uppercase
refine.RefineProject(refine.RefineServer(), projectID).text_transform(columnName, 'value.toUppercase()',on_error='set-to-blank',repeat=False, repeat_count=10)
# Edit cells-> common transforms -> to Lowercase
refine.RefineProject(refine.RefineServer(), projectID).text_transform(columnName, 'value.toLowercase()',on_error='set-to-blank',repeat=False, repeat_count=10)
# Edit cells-> common transforms -> to number
refine.RefineProject(refine.RefineServer(), projectID).text_transform(columnName, 'value.toNumber()',on_error='set-to-blank',repeat=False, repeat_count=10)
# Edit cells-> common transforms -> to date
refine.RefineProject(refine.RefineServer(), projectID).text_transform(columnName, 'value.toDate()',on_error='set-to-blank',repeat=False, repeat_count=10)
# Edit cells-> common transforms -> to text
refine.RefineProject(refine.RefineServer(), projectID).text_transform(columnName, 'value.toString()',on_error='set-to-blank',repeat=False, repeat_count=10)
# cluster and edit
# clusters:  type: 'binning'; function:'fingerprint'; params:{}
refine.RefineProject(refine.RefineServer(), projectID).compute_clusters(columnName, clusterer_type='binning', function='ngram-fingerprint', params=20)
# clusters:  type: 'knn'; function:'levenshtein'; params:{'radius':1, 'blocking-ngram-size': 6}
refine.RefineProject(refine.RefineServer(), projectID).compute_clusters(columnName, clusterer_type='knn', function='levenshtein', params={ 'radius':1,'blocking-ngram-size':6})
# mass edit: using "from" "to" mass-edit
refine.RefineProject(refine.RefineServer(), projectID).mass_edit(columnName,[{'from': [' ',' '], 'to': ' '}])
# split column
refine.RefineProject(refine.RefineServer(), projectID).split_column(columnName, separator=',', mode='separator', regex=False, guess_cell_type=True, remove_original_column=True)
# rename column
refine.RefineProject(refine.RefineServer(), projectID).rename_column(columnName, new_columnName)
# reorder columns: takes an array of column names in the new order
refine.RefineProject(refine.RefineServer(), projectID).reorder_columns(new_column_order)
# move column to a new position (like: 'end')
refine.RefineProject(refine.RefineServer(), projectID).move_column(columnName, index)
# blank down column
refine.RefineProject(refine.RefineServer(), projectID).blank_down(columnName)
# fill down columns
refine.RefineProject(refine.RefineServer(), projectID).fill_down(columnName)
# transpose columns into rows
refine.RefineProject(refine.RefineServer(), projectID).transpose_columns_into_rows(start_column, column_count, combined_column_name, separator=':', prepend_column_name=True, ignore_blank_cells=True)




