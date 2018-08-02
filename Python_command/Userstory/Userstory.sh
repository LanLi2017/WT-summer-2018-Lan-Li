#!/usr/bin/env bash

# create project from file:
python ../refine.py --create ./originaldataset/partTest.csv
python ../refine.py --apply ./OpenrefineJsonfile/Userstory1.json partTest

python ../refine.py --export partTest --output=partTest.tsv
