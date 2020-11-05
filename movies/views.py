from django.db import models
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor, Review
from .serializers import (MovieListSerializer,
                          MovieDetailSerializer,
                          ReviewCreateSerializer,
                          CreateRatingSerializer,
                          ActorListSerializer,
                          ActorDetailSerializer)
from .service import get_client_ip, MovieFilter
from .permissions import IsSuperUser


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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request))),
        ).annotate(middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings')))
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """ вывод фильма """

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewCreateView(generics.CreateAPIView):
    """ добавление отзыва к фильму """

    serializer_class = ReviewCreateSerializer
    permission_classes = [IsSuperUser]


class ReviewDestroyView(generics.DestroyAPIView):
    """ удаление отзыва к фильму """

    queryset = Review.objects.all()


class AddStarRatingView(generics.CreateAPIView):
    """ добавление рейтенга """

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
