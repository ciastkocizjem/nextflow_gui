from django.db import models
import nextflow

# Create your models here.

# class Pipeline:
#     def __init__(self, id, name, status, log, pipeline):
#         self.id = id
#         self.name = name
#         self.status = status
#         self.log = log
#         self.pipeline = pipeline

# class Template:
#     def __init__(self, id, name, pipeline):
#         self.id = id
#         self.name = name
#         self.pipeline = pipeline

class Pipeline(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    log = models.TextField(default=None, blank=True, null=True)
    pipeline_path = models.CharField(max_length=255)
    pipeline_config = models.CharField(max_length=255, default=None, blank=True, null=True)
    pipleline_parameters = models.TextField(default=None, blank=True, null=True)
    location = models.CharField(max_length=255, default="")

class Template(models.Model):
    name = models.CharField(max_length=50)
    template_path = models.CharField(max_length=255)
    template_config = models.CharField(max_length=255, default=None, blank=True, null=True)

class Parameter(models.Model):
    # pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
