from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('config', views.config, name='config'),
    path('config/<int:id>', views.configEdit, name='configEdit'),
    path('runPipe', views.PipeTest, name='PipeTest'),
    path('stopProgress', views.StopProcess, name='StopProgress'),
    path('tableData', views.TableData, name='TableData'),
    path('getPipeProg', views.PipeProgress,name='PipeProgress'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout')
]