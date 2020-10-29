from django.db import models
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Actor
from .serializers import (MovieListSerializer,
                          MovieDetailSerializer,
                          ReviewCreateSerializer,
                          CreateRatingSerializer,
                          ActorListSerializer,
                          ActorDetailSerializer)
from .service import get_client_ip


class ActorListView(generics.ListAPIView):
    """ список актеров """

    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """ актер """

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer


class MovieListView(APIView):
    """ вывод списка фильмов """

    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request))),
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """ вывод фильма """

    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """ добавление отзыва к фильму """

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
            return Response(status=201)
        else:
            return Response(status=400)


class AddStarRatingView(APIView):
    """ добавление рейтенга """

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
