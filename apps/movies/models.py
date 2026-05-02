from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    trailer_url = models.URLField(blank=True)
    poster = models.ImageField(upload_to='posters/')

    def __str__(self):
        return self.title