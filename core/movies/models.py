from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class MoviesManager(models.Model):
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    created_year = models.IntegerField()
    director = models.CharField(max_length=255)
    rate = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(10.0)
        ]
    )

    def __str__(self):
        return self.name
