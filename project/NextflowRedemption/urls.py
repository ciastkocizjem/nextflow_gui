from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('config', views.config, name='config'),
    path('config/<int:id>', views.configEdit, name='configEdit'),
    path('runPipe', views.PipeTest, name='PipeTest'),
    path('tableData', views.TableData, name='TableData'),
    path('getPipeProg', views.PipeProgress,name='PipeProgress')
]