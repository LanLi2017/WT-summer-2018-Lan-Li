#!/usr/bin/env bash

# set variables
source ../settings.sh

# create output directories
mkdir -p $FACTS_DIR
mkdir -p $VIEWS_DIR
mkdir -p $RESULTS_DIR

# export YW model facts
$YW_CMD model $SCRIPT_DIR/topic_modeling.py \
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
$YW_CMD graph $SCRIPT_DIR/topic_modeling.py \
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

# draw worfklow graph upstream of LDA_model
$QUERIES_DIR/render_wf_graph_upstream_of_data_q1.sh \'LDA_model\' > $RESULTS_DIR/wf_upstream_of_LDA_model.gv
dot -Tpdf $RESULTS_DIR/wf_upstream_of_LDA_model.gv > $RESULTS_DIR/wf_upstream_of_LDA_model.pdf
dot -Tsvg $RESULTS_DIR/wf_upstream_of_LDA_model.gv > $RESULTS_DIR/wf_upstream_of_LDA_model.svg

# draw worfklow graph upstream of LogFile
$QUERIES_DIR/render_wf_graph_upstream_of_data_q1.sh \'LogFile\' > $RESULTS_DIR/wf_upstream_of_LogFile.gv
dot -Tpdf $RESULTS_DIR/wf_upstream_of_LogFile.gv > $RESULTS_DIR/wf_upstream_of_LogFile.pdf
dot -Tsvg $RESULTS_DIR/wf_upstream_of_LogFile.gv > $RESULTS_DIR/wf_upstream_of_LogFile.svg

# draw worfklow graph upstream of dictionary
$QUERIES_DIR/render_wf_graph_upstream_of_data_q1.sh \'dictionary\' > $RESULTS_DIR/wf_upstream_of_dictionary.gv
dot -Tpdf $RESULTS_DIR/wf_upstream_of_dictionary.gv > $RESULTS_DIR/wf_upstream_of_dictionary.pdf
dot -Tsvg $RESULTS_DIR/wf_upstream_of_dictionary.gv > $RESULTS_DIR/wf_upstream_of_dictionary.svg

# draw worfklow graph upstream of Corpus
$QUERIES_DIR/render_wf_graph_upstream_of_data_q1.sh \'Corpus\' > $RESULTS_DIR/wf_upstream_of_Corpus.gv
dot -Tpdf $RESULTS_DIR/wf_upstream_of_Corpus.gv > $RESULTS_DIR/wf_upstream_of_Corpus.pdf
dot -Tsvg $RESULTS_DIR/wf_upstream_of_Corpus.gv > $RESULTS_DIR/wf_upstream_of_Corpus.svg


##############
#   Q2_pro   #
##############

# list workflow outputs
#$QUERIES_DIR/list_dependent_inputs_q2.sh > $RESULTS_DIR/#q2_pro_outputs.txt


# list script inputs upstream of output data LDA_model
$QUERIES_DIR/list_inputs_upstream_of_data_q2.sh \'LDA_model\' Topicmodeling_Result > $RESULTS_DIR/inputs_upstream_of_LDA_model.txt

# list script inputs upstream of output data LogFile
$QUERIES_DIR/list_inputs_upstream_of_data_q2.sh \'LogFile\' Topicmodeling_Result > $RESULTS_DIR/inputs_upstream_of_LogFile.txt

##############
#   Q3_pro   #
##############

# draw worfklow graph downstream of Static_text
$QUERIES_DIR/render_wf_graph_downstream_of_data_q3.sh \'Static_text\' > $RESULTS_DIR/wf_downstream_of_Static_text.gv
dot -Tpdf $RESULTS_DIR/wf_downstream_of_Static_text.gv > $RESULTS_DIR/wf_downstream_of_Static_text.pdf
dot -Tsvg $RESULTS_DIR/wf_downstream_of_Static_text.gv > $RESULTS_DIR/wf_downstream_of_Static_text.svg

# draw worfklow graph downstream of dictionary
$QUERIES_DIR/render_wf_graph_downstream_of_data_q3.sh \'dictionary\' > $RESULTS_DIR/wf_downstream_of_dictionary.gv
dot -Tpdf $RESULTS_DIR/wf_downstream_of_dictionary.gv > $RESULTS_DIR/wf_downstream_of_dictionary.pdf
dot -Tsvg $RESULTS_DIR/wf_downstream_of_dictionary.gv > $RESULTS_DIR/wf_downstream_of_dictionary.svg

# draw worfklow graph downstream of Corpus
$QUERIES_DIR/render_wf_graph_downstream_of_data_q3.sh \'Corpus\' > $RESULTS_DIR/wf_downstream_of_Corpus.gv
dot -Tpdf $RESULTS_DIR/wf_downstream_of_Corpus.gv > $RESULTS_DIR/wf_downstream_of_Corpus.pdf
dot -Tsvg $RESULTS_DIR/wf_downstream_of_Corpus.gv > $RESULTS_DIR/wf_downstream_of_Corpus.svg

##############
#   Q4_pro   #
##############

# list workflow outputs
#$QUERIES_DIR/list_dependent_outputs_q4.sh > $RESULTS_DIR/q4_pro_outputs.txt

# list script outputs downstream of input data Static_Text
$QUERIES_DIR/list_outputs_downstream_of_data_q4.sh \'Static_Text\' Static_Text > $RESULTS_DIR/outputs_downstream_of_Static_Text.txt

##############
#   Q5_pro   #
##############

# draw recon worfklow graph upstream of LDA_model
$QUERIES_DIR/render_wf_recon_graph_upstream_of_data_q5.sh \'LDA_model\' > $RESULTS_DIR/wf_recon_upstream_of_LDA_model.gv
dot -Tpdf $RESULTS_DIR/wf_recon_upstream_of_LDA_model.gv > $RESULTS_DIR/wf_recon_upstream_of_LDA_model.pdf
dot -Tsvg $RESULTS_DIR/wf_recon_upstream_of_LDA_model.gv > $RESULTS_DIR/wf_recon_upstream_of_LDA_model.svg

# draw recon worfklow graph upstream of LogFile
$QUERIES_DIR/render_wf_recon_graph_upstream_of_data_q5.sh \'LogFile\' > $RESULTS_DIR/wf_recon_upstream_of_LogFile.gv
dot -Tpdf $RESULTS_DIR/wf_recon_upstream_of_LogFile.gv > $RESULTS_DIR/wf_recon_upstream_of_LogFile.pdf
dot -Tsvg $RESULTS_DIR/wf_recon_upstream_of_LogFile.gv > $RESULTS_DIR/wf_recon_upstream_of_LogFile.svg

##############
#   Q6_pro   #
##############


# draw recon workflow graph with all observables

$QUERIES_DIR/render_recon_complete_wf_graph_q6.sh > $RESULTS_DIR/wf_recon_complete_graph_all_observables.gv
dot -Tpdf $RESULTS_DIR/wf_recon_complete_graph_all_observables.gv > $RESULTS_DIR/wf_recon_complete_graph_all_observables.pdf
dot -Tsvg $RESULTS_DIR/wf_recon_complete_graph_all_observables.gv > $RESULTS_DIR/wf_recon_complete_graph_all_observables.svg
