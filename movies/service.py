from django_filters import rest_framework as filters
from .models import Movie


def get_client_ip(request):
    """ получение IP пользователя """
    x_forwaded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwaded_for:
        ip = x_forwaded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class MovieFilter(filters.FilterSet):
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    year = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ['genres', 'year']
