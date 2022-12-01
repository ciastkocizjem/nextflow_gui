# Create your tasks here

import os
from celery import shared_task
from ast import literal_eval
#from NextflowRedemption.db_utility import save, load
import nextflow
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
        log += execution.stdout
        update_pipe.log = log
        update_pipe.save()