import django_filters
from django.db.models import Q
from .models import Operation


class OperationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Operation
        fields = ['search']

    def filter_search(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(operand1__icontains=value) |
                Q(operand2__icontains=value) |
                Q(result__icontains=value) |
                Q(operator__icontains=value) |
                Q(user__username__icontains=value)
            )
        return queryset