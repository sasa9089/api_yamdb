from django_filters.filters import CharFilter
from django_filters.rest_framework.filterset import FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='contains')
    category = CharFilter(field_name='category__slug', lookup_expr='contains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('year', 'category', 'genre', 'name')
