from django.urls import path

from search_yt.views import Index, GetSearchResults

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('search_result', GetSearchResults.as_view(), name='search_result')
]
