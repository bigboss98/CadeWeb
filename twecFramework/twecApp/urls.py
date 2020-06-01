"""
    Urls configuration for twecApp application
"""
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.urls import path
from . import views
from .views import TaskView, TaskDelete, TaskAdd, DetailsView
from .globalAnalysis import JumpersView, StablesView
from .localAnalysis import CorrespondanceView, NeighborsView, SimilarityView
urlpatterns = [
        path('task/add', TaskAdd.as_view(), name='task_add'),
        path('task/', TaskView.as_view(), name = 'task_view'),
        path('task/<int:num_task>', TaskDelete.as_view(), name = 'task_delete'),
        path('task/<int:num_task>/analysis', DetailsView.as_view(), name = 'analysis'),
        path('task/<int:num_task>/global/jumpers', JumpersView.as_view(), name = 'jumpers'),
        path('task/<int:num_task>/global/stables', StablesView.as_view(), name = 'stables'),
        path('task/<int:num_task>/local/correspondance', CorrespondanceView.as_view(), name = 'correspondance'), 
        path('task/<int:num_task>/local/neighbors', NeighborsView.as_view(), name = 'neighbors'),
        path('task/<int:num_task>/local/similarity', SimilarityView.as_view(), name = 'similarity'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, view=never_cache(serve))
