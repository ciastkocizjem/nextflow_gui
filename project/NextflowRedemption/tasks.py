# Create your tasks here

import os
from celery import shared_task
#from NextflowRedemption.db_utility import save, load
import nextflow
import pdb

from NextflowRedemption.models import Pipeline

@shared_task
def add(x, y):
    return x + y

@shared_task()
def StartPipe(idx):
    #pipes = Pipeline.objects.all()
    pipe = Pipeline.objects.get(id = idx)
    # selectedPipe = pipe.pipeline_path
    # pipename = pipe.name
    # for x in pipes:
    #     if x.id == idx:
    #         selectedPipe = x.pipeline_path
    #         pipename = x.name
    #         break
    pipelineToRun = nextflow.Pipeline(pipe.pipeline_path, pipe.pipeline_config)
    #pdb.set_trace()
    if not os.path.exists(os.path.join('./pipelines', pipe.name)):
        os.makedirs(os.path.join('./pipelines', pipe.name))
    for execution in pipelineToRun.run_and_poll(sleep=1,location="./pipelines/"+pipe.name):
        # pipes = Pipeline.objects.all()
        # Pipeline.objects.get(id = idx).delete()
        # for x in pipes:
        #     if x.id == idx:
        #         pipes.remove(x)
        #         break
        # nextflowPipe = nextflow.Pipeline(pipe.pipeline_path,pipe.pipeline_config)
        update_pipe = Pipeline.objects.get(id = idx)
        update_pipe.status = execution.status
        log = "COMMAND: " +str(execution.command)
        log += "STATUS: " +str(execution.status)+"\n"
        log += "DURATION: " +str(execution.duration)+"s\n"
        log += execution.stdout
        update_pipe.log = log
        # update = Pipeline(idx,pipe.name,execution.status,execution.log,nextflowPipe)
        # pipes.append(update)
        # save("pipeline", pipes)
        update_pipe.save()