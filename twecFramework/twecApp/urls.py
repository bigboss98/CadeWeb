"""
    Urls configuration for twecApp application
"""
from django.urls import path
from . import views
from .views import TrainView

urlpatterns = [
        path('', TrainView.as_view(), name='index'),
        path('add_document/', views.add_document, name='add_document'),
        path('remove_document/', views.remove_document, name='remove_document'),
]
