# Create your tasks here

import os
from celery import shared_task
from ast import literal_eval
#from NextflowRedemption.db_utility import save, load
import nextflow
import fnmatch
import pdb

from NextflowRedemption.models import Pipeline

@shared_task()
def StartPipe(idx):
    pipe = Pipeline.objects.get(id = idx)
    pipelineToRun = nextflow.Pipeline(pipe.pipeline_path, pipe.pipeline_config)
    params = {}
    if(pipe.pipleline_parameters != None):
        pipe_params = literal_eval(pipe.pipleline_parameters)
        for elem in pipe_params:
            params[elem[0]] = elem[1]

    params["resume"] = "-resume"
        
    if not os.path.exists(os.path.join(pipe.location, pipe.name)):
        os.makedirs(os.path.join(pipe.location, pipe.name))
    for execution in pipelineToRun.run_and_poll(sleep=1,params=params,location=os.path.join(pipe.location, pipe.name)):

        update_pipe = Pipeline.objects.get(id = idx)
        update_pipe.status = execution.status
        log = "COMMAND: " +str(execution.command)
        log += "STATUS: " +str(execution.status)+"\n"
        log += "DURATION: " +str(execution.duration)+"s\n"
        tracefile = None
        filedate = None
        #check if tracefile was generated
        for file in os.listdir(os.getcwd()):
            tempdate = os.path.getatime(os.path.join(os.getcwd(),file))
            if fnmatch.fnmatch(file, 'trace*') and (filedate == None or tempdate > filedate):
                with open(os.path.join(os.getcwd(),file)) as f:
                    tracefile = f.readlines()
                    filedate = tempdate
        # pdb.set_trace()
        if(tracefile):
            #log += "PROGRESS: "
            
            colidx = []
            cols = tracefile[0].split('\t')
            i = cols.index("hash") if "hash" in cols else None
            if(i):
                colidx.append(i)
            j = cols.index("name") if "name" in cols else None
            if(j):
                colidx.append(j)
            k = cols.index("status") if "status" in cols else None
            if(k):
                colidx.append(k)
            tracefile.pop(0)
            #pdb.set_trace()
            # if(len(execution.process_executions)==0):
            #     progr = 0
            # else:
            #     progr = round(len(tracefile)/len(execution.process_executions),0)
            # log += str(progr*100) + "%\n"
            log += "TRACEFILE: \n"
            for line in tracefile:
                cols = line.split('\t')
                log += ("[" + cols[colidx[0]] + "]\t" + cols[colidx[1]]+ "\t" + cols[colidx[2]]+"\n")
        else:
            log += "STDOUT: \n"
            log += execution.stdout
        update_pipe.log = log
        update_pipe.save()