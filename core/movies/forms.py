from django import forms
from movies.models import MoviesManager


class MovieForm(forms.ModelForm):

    class Meta:
        model = MoviesManager
        fields = ["name", "genre", "created_year", "director", "rate"]


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Query')