from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import JsonResponse
import nextflow
import pdb
from NextflowRedemption.models import Pipeline, Template
from NextflowRedemption.db_utility import save, load
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt

from NextflowRedemption.tasks import StartPipe

def index(request):
    presets = load("template")
    pipes = load("pipeline")

    save("template", presets)
    save("pipeline", pipes)
    context = { 'presets': presets, 'pipes': pipes }
    return render(request, 'NextflowRedemption/index.html', context)

def login(request):
    context = { 'x': 'x' }
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request, 'Config/index.html', context)
        else:
            raise PermissionDenied()
    return render(request, 'NextflowRedemption/login.html', context)

def logout(request):
    presets = load("template")
    pipes = load("pipeline")
    context = { 'presets': presets, 'pipes': pipes }
    auth_logout(request)
    return render(request, 'NextflowRedemption/index.html', context)

@login_required(login_url='/main/login')
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

@csrf_exempt
def PipeTest(request):
    idx = int(request.GET["nr"][0])
    #pdb.set_trace()
    StartPipe.delay(idx)
    return JsonResponse({"_":""},status=200)

@csrf_exempt
def PipeProgress(request):
    idx = int(request.GET["nr"][0])
    pipes = load("pipeline")
    selectedPipe = None
    for x in pipes:
        if x.id == idx:
            selectedPipe = x
            break
    # count = len(execProg.process_executions)
    # done = 0
    # for proc in execProg.process_executions:
    #    if(proc.status == "COMPLETED"): 
    #     done+=1
    # if(done == 0):
    #     perc = 0
    # else:
    #     perc = done/count*100
    try: selectedPipe.status; selectedPipe.log
    except: return JsonResponse({"execStatus": "running","details":"running"}, status=200)
    return JsonResponse({"execStatus": selectedPipe.status,"details":selectedPipe.log}, status=200)