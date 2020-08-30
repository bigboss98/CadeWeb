"""
    Urls configuration for twecApp application
"""
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.urls import path
from twecApp.views import DetailsView
from .globalAnalysis import JumpersView, StablesView
from .localAnalysis import CorrespondanceView, NeighborsView, SimilarityView, AnalogiesView
urlpatterns = [
        path('', DetailsView.as_view(), name='analysis'),
        path('global/jumpers', JumpersView.as_view(), name='jumpers'),
        path('global/stables', StablesView.as_view(), name='stables'),
        path('local/correspondance', CorrespondanceView.as_view(), name='correspondance'),
        path('local/neighbors', NeighborsView.as_view(), name='neighbors'),
        path('local/similarity', SimilarityView.as_view(), name='similarity'),
        path('local/analogies', AnalogiesView.as_view(), name='analogies'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, view=never_cache(serve))
