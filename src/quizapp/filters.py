import django_filters

from .models import Quiz


class QuizFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains', label='Название'
    )

    class Meta:
        model = Quiz
        fields = ['title', 'level']
