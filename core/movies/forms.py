from django import forms
from movies.models import MoviesManager


class MovieForm(forms.ModelForm):

    class Meta:
        model = MoviesManager
        fields = ["name", "genre", "created_year", "director", "rate"]