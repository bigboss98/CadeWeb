"""
    Urls configuration for twecApp application
"""
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.urls import path
from . import views
from .views import TrainView, TaskView, TaskDelete, TaskAdd
from .localAnalysis import LocalView

urlpatterns = [
        path('', TrainView.as_view(), name='index'),
        path('task/', TaskView.as_view(), name = 'task_view'),
        path('task/<int:num_task>', TaskDelete.as_view(), name = 'task_delete'),
        path('task/add/', TaskAdd.as_view(), name = 'task_add'),
        path('task/local/<int:num_task>', LocalView.as_view(), name = 'local_analysis'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, view=never_cache(serve))
