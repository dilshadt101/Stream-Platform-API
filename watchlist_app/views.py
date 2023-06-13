from django.shortcuts import render
from django.http import JsonResponse

from .models import Movie


def movie_list(request):
    movies = Movie.objects.all()
    data = {
        'movies': list(movies.values())
    }
    return JsonResponse(data)


def movie_details(request, id):
    movie = Movie.objects.get(pk=id)
    data = {
        'name': movie.name,
        'description': movie.description,
        'active': movie.active
    }
    return JsonResponse('', safe=False)
