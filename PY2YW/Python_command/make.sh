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
$YW_CMD graph $SCRIPT_DIR/json_python.py \
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

# draw worfklow graph upstream of operation_name
$QUERIES_DIR/render_wf_graph_upstream_of_data_q1.sh \'operation_name\' > $RESULTS_DIR/wf_upstream_of_operation_name.gv
dot -Tpdf $RESULTS_DIR/wf_upstream_of_operation_name.gv > $RESULTS_DIR/wf_upstream_of_operation_name.pdf
dot -Tsvg $RESULTS_DIR/wf_upstream_of_operation_name.gv > $RESULTS_DIR/wf_upstream_of_operation_name.svg

# draw worfklow graph upstream of operation_method_name
$QUERIES_DIR/render_wf_graph_upstream_of_data_q1.sh \'operation_method_name\' > $RESULTS_DIR/wf_upstream_of_operation_method_name.gv
dot -Tpdf $RESULTS_DIR/wf_upstream_of_operation_method_name.gv > $RESULTS_DIR/wf_upstream_of_operation_method_name.pdf
dot -Tsvg $RESULTS_DIR/wf_upstream_of_operation_method_name.gv > $RESULTS_DIR/wf_upstream_of_operation_method_name.svg

# draw worfklow graph upstream of operation_target
$QUERIES_DIR/render_wf_graph_upstream_of_data_q1.sh \'operation_target\' > $RESULTS_DIR/wf_upstream_of_operation_target.gv
dot -Tpdf $RESULTS_DIR/wf_upstream_of_operation_target.gv > $RESULTS_DIR/wf_upstream_of_operation_target.pdf
dot -Tsvg $RESULTS_DIR/wf_upstream_of_operation_target.gv > $RESULTS_DIR/wf_upstream_of_operation_target.svg

# draw worfklow graph upstream of raw_json_file
$QUERIES_DIR/render_wf_graph_upstream_of_data_q1.sh \'raw_json_file\' > $RESULTS_DIR/wf_upstream_of_raw_json_file.gv
dot -Tpdf $RESULTS_DIR/wf_upstream_of_raw_json_file.gv > $RESULTS_DIR/wf_upstream_of_raw_json_file.pdf
dot -Tsvg $RESULTS_DIR/wf_upstream_of_raw_json_file.gv > $RESULTS_DIR/wf_upstream_of_raw_json_file.svg


##############
#   Q2_pro   #
##############

# list workflow outputs
#$QUERIES_DIR/list_dependent_inputs_q2.sh > $RESULTS_DIR/#q2_pro_outputs.txt


# list script inputs upstream of output data operation_name
$QUERIES_DIR/list_inputs_upstream_of_data_q2.sh \'operation_name\' OJson_Result > $RESULTS_DIR/inputs_upstream_of_operation_name.txt

# list script inputs upstream of output data operation_method_name
$QUERIES_DIR/list_inputs_upstream_of_data_q2.sh \'operation_method_name\' OJson_Result > $RESULTS_DIR/inputs_upstream_of_operation_method_name.txt

# list script inputs upstream of output data operation_target
$QUERIES_DIR/list_inputs_upstream_of_data_q2.sh \'operation_target\' OJson_Result > $RESULTS_DIR/inputs_upstream_of_operation_target.txt

##############
#   Q3_pro   #
##############

# draw worfklow graph downstream of raw_json_file
$QUERIES_DIR/render_wf_graph_downstream_of_data_q3.sh \'raw_json_file\' > $RESULTS_DIR/wf_downstream_of_raw_json_file.gv
dot -Tpdf $RESULTS_DIR/wf_downstream_of_raw_json_file.gv > $RESULTS_DIR/wf_downstream_of_raw_json_file.pdf
dot -Tsvg $RESULTS_DIR/wf_downstream_of_raw_json_file.gv > $RESULTS_DIR/wf_downstream_of_raw_json_file.svg

# draw worfklow graph downstream of json_path
$QUERIES_DIR/render_wf_graph_downstream_of_data_q3.sh \'json_path\' > $RESULTS_DIR/wf_downstream_of_json_path.gv
dot -Tpdf $RESULTS_DIR/wf_downstream_of_json_path.gv > $RESULTS_DIR/wf_downstream_of_json_path.pdf
dot -Tsvg $RESULTS_DIR/wf_downstream_of_json_path.gv > $RESULTS_DIR/wf_downstream_of_json_path.svg

##############
#   Q4_pro   #
##############

# list workflow outputs
#$QUERIES_DIR/list_dependent_outputs_q4.sh > $RESULTS_DIR/q4_pro_outputs.txt

# list script outputs downstream of input data json_path
$QUERIES_DIR/list_outputs_downstream_of_data_q4.sh \'json_path\' json_path > $RESULTS_DIR/outputs_downstream_of_json_path.txt

##############
#   Q5_pro   #
##############

# draw recon worfklow graph upstream of operation_name
$QUERIES_DIR/render_wf_recon_graph_upstream_of_data_q5.sh \'operation_name\' > $RESULTS_DIR/wf_recon_upstream_of_operation_name.gv
dot -Tpdf $RESULTS_DIR/wf_recon_upstream_of_operation_name.gv > $RESULTS_DIR/wf_recon_upstream_of_operation_name.pdf
dot -Tsvg $RESULTS_DIR/wf_recon_upstream_of_operation_name.gv > $RESULTS_DIR/wf_recon_upstream_of_operation_name.svg

# draw recon worfklow graph upstream of operation_method_name
$QUERIES_DIR/render_wf_recon_graph_upstream_of_data_q5.sh \'operation_method_name\' > $RESULTS_DIR/wf_recon_upstream_of_operation_method_name.gv
dot -Tpdf $RESULTS_DIR/wf_recon_upstream_of_operation_method_name.gv > $RESULTS_DIR/wf_recon_upstream_of_operation_method_name.pdf
dot -Tsvg $RESULTS_DIR/wf_recon_upstream_of_operation_method_name.gv > $RESULTS_DIR/wf_recon_upstream_of_operation_method_name.svg

# draw recon worfklow graph upstream of operation_target
$QUERIES_DIR/render_wf_recon_graph_upstream_of_data_q5.sh \'operation_target\' > $RESULTS_DIR/wf_recon_upstream_of_operation_target.gv
dot -Tpdf $RESULTS_DIR/wf_recon_upstream_of_operation_target.gv > $RESULTS_DIR/wf_recon_upstream_of_operation_target.pdf
dot -Tsvg $RESULTS_DIR/wf_recon_upstream_of_operation_target.gv > $RESULTS_DIR/wf_recon_upstream_of_operation_target.svg

##############
#   Q6_pro   #
##############


# draw recon workflow graph with all observables

$QUERIES_DIR/render_recon_complete_wf_graph_q6.sh > $RESULTS_DIR/wf_recon_complete_graph_all_observables.gv
dot -Tpdf $RESULTS_DIR/wf_recon_complete_graph_all_observables.gv > $RESULTS_DIR/wf_recon_complete_graph_all_observables.pdf
dot -Tsvg $RESULTS_DIR/wf_recon_complete_graph_all_observables.gv > $RESULTS_DIR/wf_recon_complete_graph_all_observables.svg
