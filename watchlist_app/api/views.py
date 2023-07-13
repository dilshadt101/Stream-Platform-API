from _ast import Is

from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle

from watchlist_app.models import *
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from .throttling import ReviewCreateThrottle, ReviewListThrottle

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


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle]


    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating += 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)


# class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer


class StreamPlatformVS(viewsets.ModelViewSet):
    serializer_class = StreamPlatformSerializer
    queryset = StreamPlatform.objects.all()
    permission_classes = [IsAdminOrReadOnly]



# class StreamPlatformVS(viewsets.ViewSet):
#
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk=None):
#         pk = self.kwargs.get('pk')
#         watchlist = get_object_or_404(StreamPlatform, pk=pk)
#         watchlist.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

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


class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

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
