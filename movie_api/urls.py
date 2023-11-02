from django.urls import path

from movie_api.views import MoviesListView

app_name = 'movies'

urlpatterns = [
    path('', MoviesListView.as_view(), name='movies-list'),
]
