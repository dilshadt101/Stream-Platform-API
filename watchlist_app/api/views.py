from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from watchlist_app.models import *
from .serializers import WatchListSerializer, StreamPlatformSerializer
from django.http import JsonResponse


# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     if request.method == 'POST':
#         ser = MovieSerializer(data=request.data)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data, status=status.HTTP_200_OK)
#         else:
#             return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     movie = Movie.objects.get(pk=pk)
#     if request.method == 'GET':
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     if request.method == 'PUT':
#         ser = MovieSerializer(data=request.data, instance=movie)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data, status=status.HTTP_200_OK)
#         else:
#             return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class StreamPlatformAV(APIView):

    def get(self, request):
        platform = StreamPlatform.objects.all()
        ser = StreamPlatformSerializer(platform, many=True, context={'request': request})
        return Response(ser.data)

    def post(self, request):
        ser = StreamPlatformSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)

        return Response(ser.errors)


class StreamPlatformDetailAV(APIView):

    def get(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        ser = StreamPlatformSerializer(platform, many=True)
        return Response(ser.data)

    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        ser = StreamPlatformSerializer(data=request.data, instance=platform)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)

        return Response(ser.errors)

    def delete(self, request, pk):
        watch_list = WatchList.objects.get(pk=pk)
        watch_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAV(APIView):

    def get(self, request):
        watch_list = WatchList.objects.all()
        serializer = WatchListSerializer(watch_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser = WatchListSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailAV(APIView):

    def get(self, request, pk):
        watch_list = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(watch_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        watch_list = WatchList.objects.get(pk=pk)
        ser = WatchListSerializer(data=request.data, instance=watch_list)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        watch_list = WatchList.objects.get(pk=pk)
        watch_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
