# Create your tasks here

import os
from celery import shared_task
from NextflowRedemption.db_utility import save, load
import nextflow
import pdb

from NextflowRedemption.models import Pipeline

@shared_task
def add(x, y):
    return x + y

@shared_task()
def StartPipe(idx):
    pipes = load("pipeline")
    selectedPipe = None
    pipename = ""
    for x in pipes:
        if x.id == idx:
            selectedPipe = x.pipeline
            pipename = x.name
            break
    pipelineToRun = nextflow.Pipeline(selectedPipe.path)
    #pdb.set_trace()
    if not os.path.exists(os.path.join('./pipelines', pipename)):
        os.makedirs(os.path.join('./pipelines', pipename))
    for execution in pipelineToRun.run_and_poll(sleep=1,location="./pipelines/"+pipename):
        pipes = load("pipeline")
        for x in pipes:
            if x.id == idx:
                pipes.remove(x)
                break
        nextflowPipe = nextflow.Pipeline(selectedPipe.path,selectedPipe.config)
        update = Pipeline(idx,pipename,execution.status,execution.log,nextflowPipe)
        pipes.append(update)
        save("pipeline", pipes)