from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import JsonResponse
import nextflow
#import random
from NextflowRedemption.models import Pipeline, Template
from NextflowRedemption.db_utility import save, load

def index(request):
    presets = load("template")
    pipes = load("pipeline")
    # c = 0
    # for i in range(random.randrange(3, 10)):
    #     pipe = nextflow.Pipeline("/pipelines/pipe"+str(i),config="/configs/conf"+str(i))
    #     preset = Template(i,"preset"+str(i),pipe)
    #     presets.append(preset)
    #     pipeObj = Pipeline(i,"preset"+str(c)+"_pipe"+str(c+1),pipe)
    #     pipes.append(pipeObj)
    #     c+=1

    save("template", presets)
    save("pipeline", pipes)
    context = { 'presets': presets, 'pipes': pipes }
    return render(request, 'NextflowRedemption/index.html', context)

def config(request):
    context = { 'klucz': "test" }
    return render(request, 'Config/index.html', context)

def PipeTest(request):
    pipeline1 = nextflow.Pipeline("pipelines/my-pipeline.nf")
    #execution = pipeline1.run()
    for execution in pipeline1.run_and_poll(sleep=1):
        global execProg
        execProg = execution
    return JsonResponse({"_":""},status=200)

def PipeProgress(request):
    count = len(execProg.process_executions)
    done = 0
    for proc in execProg.process_executions:
       if(proc.status == "COMPLETED"): 
        done+=1
    if(done == 0):
        perc = 0
    else:
        perc = done/count*100
    return JsonResponse({"execStatus": execProg.status,"execPercent":perc, "done":done,"count":count}, status=200)