#!/usr/bin/env bash

# set variables
source ../settings.sh

# create output directories
mkdir -p $FACTS_DIR
mkdir -p $VIEWS_DIR
mkdir -p $RESULTS_DIR

# export YW model facts
$YW_CMD model $SCRIPT_DIR/json_python.py \
        -c extract.language=python \
        -c extract.factsfile=$FACTS_DIR/yw_extract_facts.P \
        -c model.factsfile=$FACTS_DIR/yw_model_facts.P \
        -c query.engine=xsb

# materialize views of YW facts
$QUERIES_DIR/materialize_yw_views.sh > $VIEWS_DIR/yw_views.P


# copy reconfacts.P  into facts folder
cp -f recon/reconfacts.P facts

# draw complete workflow graph
$QUERIES_DIR/render_complete_wf_graph.sh > $RESULTS_DIR/complete_wf_graph.gv
dot -Tpdf $RESULTS_DIR/complete_wf_graph.gv > $RESULTS_DIR/complete_wf_graph.pdf
dot -Tsvg $RESULTS_DIR/complete_wf_graph.gv > $RESULTS_DIR/complete_wf_graph.svg


# draw complete workflow graph with URI template
$YW_CMD graph $SCRIPT_DIR/SP-ExtendedWF.json \
        -c graph.view=combined \
        -c graph.layout=tb \
        > $RESULTS_DIR/complete_wf_graph_uri.gv
dot -Tpdf $RESULTS_DIR/complete_wf_graph_uri.gv > $RESULTS_DIR/complete_wf_graph_uri.pdf
dot -Tsvg $RESULTS_DIR/complete_wf_graph_uri.gv > $RESULTS_DIR/complete_wf_graph_uri.svg


# list workflow outputs
$QUERIES_DIR/list_workflow_outputs.sh > $RESULTS_DIR/workflow_outputs.txt


##############
#   Q1_pro   #
##############

# draw worfklow graph upstream of dtable-cleaned
$QUERIES_DIR/render_wf_graph_upstream_of_data_q1.sh \'dtable-cleaned\' > $RESULTS_DIR/wf_upstream_of_dtable-cleaned.gv
dot -Tpdf $RESULTS_DIR/wf_upstream_of_dtable-cleaned.gv > $RESULTS_DIR/wf_upstream_of_dtable-cleaned.pdf
dot -Tsvg $RESULTS_DIR/wf_upstream_of_dtable-cleaned.gv > $RESULTS_DIR/wf_upstream_of_dtable-cleaned.svg

# draw worfklow graph upstream of dtable0
$QUERIES_DIR/render_wf_graph_upstream_of_data_q1.sh \'dtable0\' > $RESULTS_DIR/wf_upstream_of_dtable0.gv
dot -Tpdf $RESULTS_DIR/wf_upstream_of_dtable0.gv > $RESULTS_DIR/wf_upstream_of_dtable0.pdf
dot -Tsvg $RESULTS_DIR/wf_upstream_of_dtable0.gv > $RESULTS_DIR/wf_upstream_of_dtable0.svg

# draw worfklow graph upstream of dtable1
$QUERIES_DIR/render_wf_graph_upstream_of_data_q1.sh \'dtable1\' > $RESULTS_DIR/wf_upstream_of_dtable1.gv
dot -Tpdf $RESULTS_DIR/wf_upstream_of_dtable1.gv > $RESULTS_DIR/wf_upstream_of_dtable1.pdf
dot -Tsvg $RESULTS_DIR/wf_upstream_of_dtable1.gv > $RESULTS_DIR/wf_upstream_of_dtable1.svg

# draw worfklow graph upstream of dtable2
$QUERIES_DIR/render_wf_graph_upstream_of_data_q1.sh \'dtable2\' > $RESULTS_DIR/wf_upstream_of_dtable2.gv
dot -Tpdf $RESULTS_DIR/wf_upstream_of_dtable2.gv > $RESULTS_DIR/wf_upstream_of_dtable2.pdf
dot -Tsvg $RESULTS_DIR/wf_upstream_of_dtable2.gv > $RESULTS_DIR/wf_upstream_of_dtable2.svg

# draw worfklow graph upstream of dtable3
$QUERIES_DIR/render_wf_graph_upstream_of_data_q1.sh \'dtable3\' > $RESULTS_DIR/wf_upstream_of_dtable3.gv
dot -Tpdf $RESULTS_DIR/wf_upstream_of_dtable3.gv > $RESULTS_DIR/wf_upstream_of_dtable3.pdf
dot -Tsvg $RESULTS_DIR/wf_upstream_of_dtable3.gv > $RESULTS_DIR/wf_upstream_of_dtable3.svg

# draw worfklow graph upstream of dtable
$QUERIES_DIR/render_wf_graph_upstream_of_data_q1.sh \'dtable\' > $RESULTS_DIR/wf_upstream_of_dtable.gv
dot -Tpdf $RESULTS_DIR/wf_upstream_of_dtable.gv > $RESULTS_DIR/wf_upstream_of_dtable.pdf
dot -Tsvg $RESULTS_DIR/wf_upstream_of_dtable.gv > $RESULTS_DIR/wf_upstream_of_dtable.svg
##############
#   Q2_pro   #
##############

# list workflow outputs
#$QUERIES_DIR/list_dependent_inputs_q2.sh > $RESULTS_DIR/#q2_pro_outputs.txt


# list script inputs upstream of output data dtable-cleaned
$QUERIES_DIR/list_inputs_upstream_of_data_q2.sh \'dtable-cleaned\' OJson_Result > $RESULTS_DIR/inputs_upstream_of_dtable-cleaned.txt


##############
#   Q3_pro   #
##############

# draw worfklow graph downstream of projectName
$QUERIES_DIR/render_wf_graph_downstream_of_data_q3.sh \'projectName\' > $RESULTS_DIR/wf_downstream_of_projectName.gv
dot -Tpdf $RESULTS_DIR/wf_downstream_of_projectName.gv > $RESULTS_DIR/wf_downstream_of_projectName.pdf
dot -Tsvg $RESULTS_DIR/wf_downstream_of_projectName.gv > $RESULTS_DIR/wf_downstream_of_projectName.svg

# draw worfklow graph downstream of inputDataSetPath
$QUERIES_DIR/render_wf_graph_downstream_of_data_q3.sh \'inputDataSetPath\' > $RESULTS_DIR/wf_downstream_of_inputDataSetPath.gv
dot -Tpdf $RESULTS_DIR/wf_downstream_of_inputDataSetPath.gv > $RESULTS_DIR/wf_downstream_of_inputDataSetPath.pdf
dot -Tsvg $RESULTS_DIR/wf_downstream_of_inputDataSetPath.gv > $RESULTS_DIR/wf_downstream_of_inputDataSetPath.svg

# draw worfklow graph downstream of dtable
$QUERIES_DIR/render_wf_graph_downstream_of_data_q3.sh \'dtable\' > $RESULTS_DIR/wf_downstream_of_dtable.gv
dot -Tpdf $RESULTS_DIR/wf_downstream_of_dtable.gv > $RESULTS_DIR/wf_downstream_of_dtable.pdf
dot -Tsvg $RESULTS_DIR/wf_downstream_of_dtable.gv > $RESULTS_DIR/wf_downstream_of_dtable.svg

# draw worfklow graph downstream of dtable0
$QUERIES_DIR/render_wf_graph_downstream_of_data_q3.sh \'dtable0\' > $RESULTS_DIR/wf_downstream_of_dtable0.gv
dot -Tpdf $RESULTS_DIR/wf_downstream_of_dtable0.gv > $RESULTS_DIR/wf_downstream_of_dtable0.pdf
dot -Tsvg $RESULTS_DIR/wf_downstream_of_dtable0.gv > $RESULTS_DIR/wf_downstream_of_dtable0.svg

# draw worfklow graph downstream of dtable1
$QUERIES_DIR/render_wf_graph_downstream_of_data_q3.sh \'dtable1\' > $RESULTS_DIR/wf_downstream_of_dtable1.gv
dot -Tpdf $RESULTS_DIR/wf_downstream_of_dtable1.gv > $RESULTS_DIR/wf_downstream_of_dtable1.pdf
dot -Tsvg $RESULTS_DIR/wf_downstream_of_dtable1.gv > $RESULTS_DIR/wf_downstream_of_dtable1.svg

# draw worfklow graph downstream of dtable2
$QUERIES_DIR/render_wf_graph_downstream_of_data_q3.sh \'dtable2\' > $RESULTS_DIR/wf_downstream_of_dtable2.gv
dot -Tpdf $RESULTS_DIR/wf_downstream_of_dtable2.gv > $RESULTS_DIR/wf_downstream_of_dtable2.pdf
dot -Tsvg $RESULTS_DIR/wf_downstream_of_dtable2.gv > $RESULTS_DIR/wf_downstream_of_dtable2.svg

# draw worfklow graph downstream of dtable3
$QUERIES_DIR/render_wf_graph_downstream_of_data_q3.sh \'dtable3\' > $RESULTS_DIR/wf_downstream_of_dtable3.gv
dot -Tpdf $RESULTS_DIR/wf_downstream_of_dtable3.gv > $RESULTS_DIR/wf_downstream_of_dtable3.pdf
dot -Tsvg $RESULTS_DIR/wf_downstream_of_dtable3.gv > $RESULTS_DIR/wf_downstream_of_dtable3.svg



##############
#   Q4_pro   #
##############

# list workflow outputs
#$QUERIES_DIR/list_dependent_outputs_q4.sh > $RESULTS_DIR/q4_pro_outputs.txt

# list script outputs downstream of input data projectName
$QUERIES_DIR/list_outputs_downstream_of_data_q4.sh \'projectName\' projectName > $RESULTS_DIR/outputs_downstream_of_projectName.txt

# list script outputs downstream of input data inputDatasetPath
$QUERIES_DIR/list_outputs_downstream_of_data_q4.sh \'inputDatasetPath\' inputDatasetPath > $RESULTS_DIR/outputs_downstream_of_inputDatasetPath.txt

##############
#   Q5_pro   #
##############

# draw recon worfklow graph upstream of dtable-cleaned
$QUERIES_DIR/render_wf_recon_graph_upstream_of_data_q5.sh \'dtable-cleaned\' > $RESULTS_DIR/wf_recon_upstream_of_dtable-cleaned.gv
dot -Tpdf $RESULTS_DIR/wf_recon_upstream_of_dtable-cleaned.gv > $RESULTS_DIR/wf_recon_upstream_of_dtable-cleaned.pdf
dot -Tsvg $RESULTS_DIR/wf_recon_upstream_of_dtable-cleaned.gv > $RESULTS_DIR/wf_recon_upstream_of_dtable-cleaned.svg

##############
#   Q6_pro   #
##############


# draw recon workflow graph with all observables

$QUERIES_DIR/render_recon_complete_wf_graph_q6.sh > $RESULTS_DIR/wf_recon_complete_graph_all_observables.gv
dot -Tpdf $RESULTS_DIR/wf_recon_complete_graph_all_observables.gv > $RESULTS_DIR/wf_recon_complete_graph_all_observables.pdf
dot -Tsvg $RESULTS_DIR/wf_recon_complete_graph_all_observables.gv > $RESULTS_DIR/wf_recon_complete_graph_all_observables.svg
