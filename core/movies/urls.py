from django.urls import path
from movies.views import (
    HomePageView,
    AddMovieView,
    MovieListView,
    UpdateMovieView,
    MovieDeleteView,
    SearchMovieView,
    search_movies_api,
)

app_name = 'movies'

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('add/', AddMovieView.as_view(), name="add-movie"),
    path('list/', MovieListView.as_view(), name="list-movie"),
    path('update/<int:pk>/', UpdateMovieView.as_view(), name="update-movie"),
    path('delete/<int:pk>/', MovieDeleteView.as_view(), name="delete-movie"),

    path('search/', SearchMovieView.as_view(), name='search'),
    path('search/api/', search_movies_api, name='search_api'),


]
