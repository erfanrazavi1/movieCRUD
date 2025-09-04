from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q
from django.http import JsonResponse
from movies.forms import MovieForm, SearchForm
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

    
    

class SearchMovieView(ListView):
    model = MoviesManager
    template_name = 'CRUD/list.html'
    context_object_name = 'movies'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        form = SearchForm(self.request.GET or None)

        if form.is_valid() and form.cleaned_data.get('query'):
            query = form.cleaned_data.get('query')
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(genre__icontains=query) | Q(director__icontains=query)
                )
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET or None)
        return context

def search_movies_api(request):
    query = request.GET.get('query', '')
    movies = MoviesManager.objects.all()
    if query:
        movies = movies.filter(
            Q(name__icontains=query) | Q(genre__icontains=query) | Q(director__icontains=query)
        )
    data = [
        {
            'id': movie.id,
            'name': movie.name,
            'genre': movie.genre,
            'director': movie.director,
            'created_year': movie.created_year,
            'rate': movie.rate,
            'created_at': movie.created_at.strftime('%Y-%m-%d')
        } for movie in movies
    ]
    return JsonResponse({'movies': data})