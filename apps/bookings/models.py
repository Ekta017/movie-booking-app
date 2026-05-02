from django.db import models
from django.contrib.auth.models import User
from apps.movies.models import Movie
from django.utils import timezone


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seats = models.CharField(max_length=200)
    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.movie}"

class SeatReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.CharField(max_length=10)
    reserved_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.reserved_at + timezone.timedelta(minutes=5)