from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from movies.forms import MovieForm
from movies.models import MoviesManager
# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'

class AddMovieView(CreateView):
    model = MoviesManager
    form_class = MovieForm
    template_name = 'CRUD/add.html'
    success_url = '/'


class MovieListView(ListView):
    model = MoviesManager
    template_name = 'CRUD/list.html'
    context_object_name = 'movies' 
    paginate_by = 1

class UpdateMovieView(UpdateView):
    model = MoviesManager
    form_class = MovieForm
    template_name = 'CRUD/update.html'
    context_object_name = 'movie'
    success_url = '/'

class MovieDeleteView(DeleteView):
    model = MoviesManager
    success_url = '/'
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    
    
    