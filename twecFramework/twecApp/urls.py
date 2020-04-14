"""
    Urls configuration for twecApp application
"""
from django.urls import path
from . import views
from .views import TrainView, TaskView, TaskDelete, TaskAdd

urlpatterns = [
        path('', TrainView.as_view(), name='index'),
        path('task/', TaskView.as_view(), name = 'task_view'),
        path('task/<int:num_task>', TaskDelete.as_view(), name = 'task_delete'),
        path('task/add/', TaskAdd.as_view(), name = 'task_add'),
        path('add_document/', views.add_document, name='add_document'),
        path('remove_document/', views.remove_document, name='remove_document'),
]
