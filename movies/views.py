from django.db import models
from rest_framework import generics


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


class MovieListView(generics.ListAPIView):
    """ вывод списка фильмов """

    serializer_class = MovieListSerializer

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request))),
        ).annotate(middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings')))
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """ вывод фильма """

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    """ добавление отзыва к фильму """

    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    """ добавление рейтенга """

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
