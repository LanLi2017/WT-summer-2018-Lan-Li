Backwards Compatible Extended System  with Yesworkflow Model
=====================================

#### Reference
- [Openrefine-Client Library ](https://github.com/opencultureconsulting/openrefine-client)
- [Yesworkflow](https://github.com/yesworkflow-org/yw-prototypes)



#### Problem of the Original Openrefine 

1. Limited transparency

#### User Story 1...

- OH(operation history) as retrospective prov is not complete enough

- when the user use OH to do past auditing, find some operation in OH is opaque.
    
    Ex Q. where did all these mass-edits come from? How did they come about? 
    
    Ex Ans. cluster type: key collision/ nearest neighbor ;  cluster method: fingerprint/n-gram fingerprint n=/ metaphone3…
user will choose these parameters to do deduplicate. 

- Solution: review & revise (extend) the OR-OH model to allow for execution, eg. add new “op-name” such “cluster_and_relabel”; add new cluster infos for the cluster_and_relabel parameters.

2. Limited reusability

#### User Story 2...

- OH as prospective prov is not complete enough

- when users apply the OH to the new dataset, mass-edit re-applied might not “get the job done” (eg. new vocabulary has no matched clusters!) The missing part need to be captured and added to OH, which we called it “Extended OH”

     - Ex Q. Can we reproduce the workflow via “Extended OH”?
     
     - Ex Ans. Use Openrefine-client library to generate the Extended workflow, which includes “missing prospective” part. And then use Trans&Reproduce system to re-execute the workflow.


3. Limited structure 

#### User Story 3...

OH in OR is linear pipeline, which can not stand for the actual structure of the Data wrangling workflow. User uses Yesworkflow model to refine the workflow into Serial-Parallel model. 

Q: How can we get the actual structure of the Data wrangling workflow?

Steps:

1. Auto transfer the workflow into Yesworkflow outline file (--purpose ==)

2. Using yw configure file to graph the Serial-Parallel model.


#### Main Software

1. Using BC-X-OR-X system (Backwards Compatible Extended OpenRefine Execute) to generate the Hybrid workflow (Add missing cluster info to the mass-edit operation)

2. Using BC_trans&reproduce to transfer the hybrid workflow into Original OR workflow through Openrefine server

3. Using Yesworkflow model to generate the original Linear pipeline workflow into Linear and Serial-Parallel structure



#### Structure of the Repo

Directory            | Description
---------------------|-----------
facts                | Yesworkflow facts
pdf                  | Using Yesworkflow graph command and generate pdf file
png                  | Using Yesworkflow graph command and generate png file
script               | Python scripts to generate two modes yw model: Linear/Serial-Parallel, with the help of the Config.py command
yw                   | Outputs of the script/.py(outline files of the yw)
BC-X-OR-X.py         | Backwards Compatible BC-X-OR-X system which can generate the reproducible json file
BC_trans&reproduce.py| transfer the hybrid workflow into original Openrefine workflow through Openrefine server
HybridWF.json        | Add missing prospective part (cluster info of "mass-edit" operations) to the Original OR workflow
Menupart.csv         | Dataset from NYPL 
OpenRefinerecipe.py  | Invoke all of the Openrefine operations 
OriginalOR.json      | Original openrefine workflow 
yw.properties        | yw configuration settings
yw_generate.sh       | commands
