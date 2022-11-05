from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
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