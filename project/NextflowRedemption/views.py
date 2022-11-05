from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import nextflow
import random

class PipelineObject(object):
    id = -1
    name = ""
    pipeline = ""
    def __init__(self, id, name, pipe):
        self.id = id
        self.name = name
        self.pipeline = pipe

def index(request):
    presets = []
    pipes = []
    c = 0
    for i in range(random.randrange(3, 10)):
        pipe = nextflow.Pipeline("/pipelines/pipe"+str(i),config="/configs/conf"+str(i))
        preset = PipelineObject(i,"preset"+str(i),pipe)
        presets.append(preset)
        pipeObj = PipelineObject(i,"preset"+str(c)+"_pipe"+str(c+1),pipe)
        pipes.append(pipeObj)
        c+=1
        
    context = { 'presets': presets, 'pipes': pipes }
    return render(request, 'NextflowRedemption/index.html', context)

def config(request):
    context = { 'klucz': "test" }
    return render(request, 'Config/index.html', context)