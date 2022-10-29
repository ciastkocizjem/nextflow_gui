from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def index(request):
    context = { 'klucz': "test" }
    return render(request, 'NextflowRedemption/index.html', context)
    #return HttpResponse("Hello, world.")

def config(request):
    context = { 'klucz': "test" }
    return render(request, 'Config/index.html', context)