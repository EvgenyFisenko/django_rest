from django.urls import path

from . import views
from . import api

urlpatterns = [
    path('actor/', views.ActorViewSet.as_view({'get': 'list'})),
    path('actor/<int:pk>/', views.ActorViewSet.as_view({'get': 'retrieve'})),
    path('movie/', views.MovieViewSet.as_view({'get': 'list'})),
    path('movie/<int:pk>/', views.MovieViewSet.as_view({'get': 'retrieve'})),
    path('review/', views.ReviewCreateViewSet.as_view({'post': 'create'})),
    path('rating/', views.AddStarRatingViewSet.as_view({'post': 'create'})),
]


# urlpatterns = [
#     path('movies/', views.MovieListView.as_view()),
#     path('movie/<int:pk>/', views.MovieDetailView.as_view()),
#
#     path('review/', views.ReviewCreateView.as_view()),
#     path('review/<int:pk>/', views.ReviewDestroyView.as_view()),
#
#     path('rating/', views.AddStarRatingView.as_view()),
#     path('actors/', views.ActorListView.as_view()),
#     path('actor/<int:pk>/', views.ActorDetailView.as_view()),
#
#     path('actor-set/', api.ActorViewSet.as_view({'get': 'list'})),
#     path('actor-set/<int:pk>/', api.ActorViewSet.as_view({'get': 'retrieve'})),
# ]
