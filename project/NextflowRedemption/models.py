from django.db import models
import nextflow

# Create your models here.

class Pipeline:
    def __init__(self, id, name, pipeline):
        self.id = id
        self.name = name
        self.pipeline = pipeline

class Template:
    def __init__(self, id, name, pipeline):
        self.id = id
        self.name = name
        self.pipeline = pipeline

class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
