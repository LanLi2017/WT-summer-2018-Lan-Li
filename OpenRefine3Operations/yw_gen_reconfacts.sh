#!/usr/bin/env bash
alias yw='java -jar ~/yesworkflow-0.2.2.0-SNAPSHOT-jar-with-dependencies.jar'

yw recon json_python.py -c recon.comment='//' -c recon.factsfile=reconfacts.P






$ cat Text_facet.json | yw graph -c extract.comment='//' > Text_facet.gv
$ dot -Tpng Text_facet.gv -o Text_facet.png

