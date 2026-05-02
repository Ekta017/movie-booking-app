from django.shortcuts import render
from .models import Movie

def movie_list(request):
    genre = request.GET.get('genre')
    language = request.GET.get('language')

    movies = Movie.objects.all()

    if genre:
        movies = movies.filter(genre__iexact=genre)

    if language:
        movies = movies.filter(language__iexact=language)

    # for dropdown options (unique values)
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    languages = Movie.objects.values_list('language', flat=True).distinct()

    context = {
        'movies': movies,
        'genres': genres,
        'languages': languages,
        'selected_genre': genre,
        'selected_language': language,
    }

    return render(request, 'movies/movie_list.html', context)
