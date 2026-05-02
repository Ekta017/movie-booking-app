from django.urls import path
from .views import create_booking

urlpatterns = [
    path('book/<int:movie_id>/', create_booking, name='book_movie'),
]