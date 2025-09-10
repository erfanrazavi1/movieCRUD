from django.contrib import admin
from movies.models import MoviesManager


class MoviesAdmin(admin.ModelAdmin):
    list_display = ("name", "genre", "created_year", "director", "rate")
    search_fields = ("name", "genre", "director")
    list_filter = ("genre", "created_year", "rate")


admin.site.register(MoviesManager, MoviesAdmin)
