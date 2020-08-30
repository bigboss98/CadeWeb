"""
    Urls configuration for twecApp application
"""
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.urls import path, include
from .views import TaskView, TaskDelete, TaskAdd
urlpatterns = [
        path('task/add', TaskAdd.as_view(), name='task_add'),
        path('', TaskView.as_view(), name='task_view'),
        path('task/<int:num_task>', TaskDelete.as_view(), name='task_delete'),
        path('task/<int:num_task>/analysis/', include('twecApp.analysis.urls')),
]
