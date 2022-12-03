from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
import nextflow
import pdb
import os
import shutil
from NextflowRedemption.models import Pipeline, Template, Parameter
#from NextflowRedemption.db_utility import save, load
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from celery import current_app, current_task
from project.celery import app, debug_task

from NextflowRedemption.tasks import StartPipe
import signal

def index(request):
    presets = Template.objects.all()
    pipes = Pipeline.objects.all()

    # save("template", presets)
    # save("pipeline", pipes)
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
    presets = Template.objects.all()
    pipes = Pipeline.objects.all()
    context = { 'presets': presets, 'pipes': pipes }
    auth_logout(request)
    return render(request, 'NextflowRedemption/index.html', context)

@login_required(login_url='/main/login')
def config(request):
    if(request.method == 'POST'):
        presets = Template.objects.all()
        data = request.POST
        name = data.get("name")
        pipeline = data.get("pipeline")
        print(request.FILES)
        config = data.get("config")
        new_preset = Template.objects.create(name=name, template_path=pipeline, template_config=config)
        # presets.append({
        #     "py/object": "NextflowRedemption.models.Template",
		#     "id": len(presets),
		#     "name": name,
		#     "pipeline": {
		# 	    "py/object": "nextflow.pipeline.Pipeline",
		# 	    "path": pipeline,
		# 	    "config": config
		#     }
        # })
        new_preset.save()
        presets = Template.objects.all()
        pipes = Pipeline.objects.all()
        # save("template", presets)
        # save("pipeline", pipes)
        context = { 'presets': presets, 'pipes': pipes }
        return render(request, 'NextflowRedemption/index.html', context)
    presets = Template.objects.all()
    pipes = Pipeline.objects.all()
    context = { 'presets': presets, 'pipes': pipes}
    return render(request, 'Config/index.html', context)

def saveConfig(request):
    presets = Template.objects.all()
    pipes = Pipeline.objects.all()
    data = request.POST
    idx = data.get("id")
    name = Template.objects.get(id = idx).name + "_" + data.get("name")
    pipeline = Template.objects.get(id = idx).template_path
    config = Template.objects.get(id = idx).template_config
    exec_location = data.get("location")
    pipeline_parametsrs = data.get("table")
    #dodać parametry bo teraz chyba nie są nawet zczytywane z widoku

    new_pipe = Pipeline.objects.create(name=name, pipeline_path=pipeline, pipeline_config=config, location=exec_location, pipleline_parameters=pipeline_parametsrs)
    new_pipe.save()
    return JsonResponse({"_": ""}, status=200)

def configEdit(request, id=None):
    presets = Template.objects.all().values()
    pipes = Pipeline.objects.all().values()
    parameters = Parameter.objects.all().values()
    context = { 'preset': Template.objects.get(id = id), 'presets': presets, 'parameters': parameters}
    return render(request, 'Config/edit.html', context) 

@login_required(login_url='/main/login')
def configDelete(request):
    presets = Template.objects.all()
    context = {'presets' : presets}
    return render(request, 'Config/delete.html', context)

@login_required(login_url='/main/login')
def configActualDelete(request, id=None):
    presets = Template.objects.all().values()
    Template.objects.get(id = id).delete()
    context = {'presets' : presets}
    return render(request, 'Config/delete.html', context)

def pipelineDelete(request):
    id = int(request.GET["id"])
    Pipeline.objects.get(id = id).delete()
    presets = Template.objects.all().values()
    pipes = Pipeline.objects.all().values()
    context = { 'presets': presets, 'pipes': pipes }
    return render(request, 'NextflowRedemption/index.html', context)


def TableData(request):
    data = request.POST
    print(data.get('table'))

    # parameter = Parameter.objects.create(
    #     id=None,
    #     name=data.get('name'),
    #     value=data.get('value')
    # )
    # parameter.save()
    # val1 = request.POST['table']
    # print(val1)
    return JsonResponse({"_":""},status=200)

@csrf_exempt
def StopProcess(request):
    i = app.control.inspect()
    active = i.active()
    key = list(active.keys())[0]
    id = active[key][0]['id']
    app.control.revoke(id, terminate=True, signal='SIGTERM')
    return JsonResponse({"_":""},status=200)
    
@csrf_exempt
def PipeTest(request):
    idx = int(request.GET["nr"])
    #pdb.set_trace()
    StartPipe.delay(idx)
    return JsonResponse({"_":""},status=200)

@csrf_exempt
def PipeProgress(request):
    idx = int(request.GET["nr"])
    pipes = Pipeline.objects.all()
    selectedPipe = None
    for x in pipes:
        if x.id == idx:
            selectedPipe = x
            break
    if selectedPipe.log == None:
        return JsonResponse({"execStatus": "running","details":"running"}, status=200)
    #pdb.set_trace()
    loglines = selectedPipe.log.split("\n")
    progline = [i for i in loglines if "PROGRESS" in i]
    if(len(progline) > 0):
        progline = progline[0].replace("PROGRESS: ","").replace("%","")
        return JsonResponse({"execStatus": selectedPipe.status,"details":selectedPipe.log,"progress":progline}, status=200)
    else:
        return JsonResponse({"execStatus": selectedPipe.status,"details":selectedPipe.log}, status=200)

@csrf_exempt
def ResetPipe(request):
    idx = int(request.POST["nr"])
    #Pipeline.objects.get(id = idx).delete()
    reset_pipe = Pipeline.objects.get(id = idx)
    reset_pipe.status = ""
    reset_pipe.log = None
    reset_pipe.save()
    if os.path.exists(os.path.join(reset_pipe.location, reset_pipe.name)):
        shutil.rmtree(os.path.join(reset_pipe.location, reset_pipe.name))
    return JsonResponse({"id": idx}, status=200)