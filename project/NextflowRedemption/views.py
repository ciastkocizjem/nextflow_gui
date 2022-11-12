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
    if(request.method == 'POST'):
        presets = load("template")
        data = request.POST
        name = data.get("name")
        pipeline = request.FILES.get("pipeline")
        print(request.FILES)
        config = request.FILES.get("config")
        presets.append({
            "py/object": "NextflowRedemption.models.Template",
		    "id": len(presets),
		    "name": name,
		    "pipeline": {
			    "py/object": "nextflow.pipeline.Pipeline",
			    "path": pipeline,
			    "config": config
		    }
        })
        pipes = load("pipeline")
        save("template", presets)
        save("pipeline", pipes)
        context = { 'presets': presets, 'pipes': pipes }
        return render(request, 'NextflowRedemption/index.html', context)
    presets = load("template")
    pipes = load("pipeline")
    context = { 'presets': presets, 'pipes': pipes}
    return render(request, 'Config/index.html', context)

def configEdit(request, id=None):
    if(request.method == 'POST'):
        pipes = load("pipeline")
        presets = load("template")
        data = request.POST
        name = presets[id].name + "_" + data.get("name")
        pipeline = data.get("pipeline")
        config = data.get("config")
        pipes.append({
            "py/object": "NextflowRedemption.models.Pipeline",
		    "id": len(pipes),
		    "name": name,
		    "pipeline": {
			    "py/object": "nextflow.pipeline.Pipeline",
			    "path": pipeline,
			    "config": config,
                "parameters": [
                    {"name": "aaaa", "value": "bbbb"},
                    {"name": "aaaa", "value": "bbbb"}
                ]
		    }
        })
        save("pipeline", pipes)
        presets = load("template")
        pipes = load("pipeline")
        context = { 'presets': presets, 'pipes': pipes }
        return render(request, 'NextflowRedemption/index.html', context)
    presets = load("template")
    pipes = load("pipeline")
    context = { 'preset': presets[id]}
    return render(request, 'Config/edit.html', context)

def TableData(request):
    val1 = request.POST['table']
    return JsonResponse({"_":""},status=200)


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