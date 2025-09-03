from django.urls import path
from movies.views import (
    HomePageView
)


urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    # path('add', AddMoviewView.as_view(), name="add-movie"),
    # path('list', MovieListView.as_view(), name="list-movie"),
    # path('update/<int:pk>', UpdateMovieView.as_view(), name="update-movie"),
    # path('delete/<int:pk>', DeleteMovieView.as_view(), name="delete-movie"),


]
