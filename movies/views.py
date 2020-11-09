from django.db import models
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor, Review
from .serializers import (MovieListSerializer,
                          MovieDetailSerializer,
                          ReviewCreateSerializer,
                          CreateRatingSerializer,
                          ActorListSerializer,
                          ActorDetailSerializer)
from .service import get_client_ip, MovieFilter


# переписываем все на ReadOnlyModelViewSet

class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод актеров или режиссеров"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == "retrieve":
            return ActorDetailSerializer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка фильмов"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == "retrieve":
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


# class ActorListView(generics.ListAPIView):
#     """ список актеров """
#
#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializer
#
#
# class ActorDetailView(generics.RetrieveAPIView):
#     """ актер """
#
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializer
#
#
# class MovieListView(generics.ListAPIView):
#     """ вывод списка фильмов """
#
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request))),
#         ).annotate(middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings')))
#         return movies
#
#
# class MovieDetailView(generics.RetrieveAPIView):
#     """ вывод фильма """
#
#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#
# class ReviewCreateView(generics.CreateAPIView):
#     """ добавление отзыва к фильму """
#
#     serializer_class = ReviewCreateSerializer
#
#
# class ReviewDestroyView(generics.DestroyAPIView):
#     """ удаление отзыва к фильму """
#
#     queryset = Review.objects.all()
#
#
# class AddStarRatingView(generics.CreateAPIView):
#     """ добавление рейтенга """
#
#     serializer_class = CreateRatingSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))
