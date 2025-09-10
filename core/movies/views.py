from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    View,
)
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from movies.forms import MovieForm, SearchForm
from movies.models import MoviesManager


class HomePageView(TemplateView):
    template_name = "home.html"


class AddMovieView(LoginRequiredMixin, CreateView):
    model = MoviesManager
    form_class = MovieForm
    template_name = "CRUD/add.html"
    success_url = "/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MovieListView(ListView):
    model = MoviesManager
    template_name = "CRUD/list.html"
    context_object_name = "movies"
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get("sort", "newest")
        if sort == "newest":
            return queryset.order_by("-created_at")
        elif sort == "oldest":
            return queryset.order_by("created_at")
        elif sort == "highest_rate":
            return queryset.order_by("-rate")
        elif sort == "lowest_rate":
            return queryset.order_by("rate")
        return queryset.order_by("-created_at")


class UpdateMovieView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MoviesManager
    form_class = MovieForm
    template_name = "CRUD/update.html"
    context_object_name = "movie"
    success_url = "/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        movie = self.get_object()
        return movie.author == self.request.user


class MovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MoviesManager
    success_url = "/"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def test_func(self):
        movie = self.get_object()
        return movie.author == self.request.user


class SearchMovieView(ListView):
    model = MoviesManager
    template_name = "CRUD/list.html"
    context_object_name = "movies"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        form = SearchForm(self.request.GET or None)
        if form.is_valid() and form.cleaned_data.get("query"):
            query = form.cleaned_data.get("query")
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(genre__icontains=query)
                | Q(director__icontains=query)
            )
        sort = self.request.GET.get("sort", "newest")
        if sort == "newest":
            return queryset.order_by("-created_at")
        elif sort == "highest_rate":
            return queryset.order_by("-rate")
        elif sort == "lowest_rate":
            return queryset.order_by("rate")
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm(self.request.GET or None)
        return context


class SearchMoviesAPIView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("query", "")
        sort = request.GET.get("sort", "newest")
        movies = MoviesManager.objects.all()

        if query:
            movies = movies.filter(
                Q(name__icontains=query)
                | Q(genre__icontains=query)
                | Q(director__icontains=query)
            )

        if sort == "newest":
            movies = movies.order_by("-created_at")
        elif sort == "highest_rate":
            movies = movies.order_by("-rate")
        elif sort == "lowest_rate":
            movies = movies.order_by("rate")
        else:
            movies = movies.order_by("-created_at")

        data = [
            {
                "id": movie.id,
                "name": movie.name,
                "genre": movie.genre,
                "director": movie.director,
                "created_year": movie.created_year,
                "rate": movie.rate,
                "created_at": movie.created_at.strftime("%Y-%m-%d"),
            }
            for movie in movies
        ]
        return JsonResponse({"movies": data})
