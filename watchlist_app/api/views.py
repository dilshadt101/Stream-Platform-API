from rest_framework.decorators import api_view
from rest_framework.response import Response
from watchlist_app.models import Movie

from .serializers import MovieSerializer
from django.http import JsonResponse


@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        ser = MovieSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_details(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    if request.method == 'PUT':
        ser = MovieSerializer(data=request.data, instance=movie)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors)

    if request.method == 'DELETE':
        movie.delete()
        return Response('Deleted')
