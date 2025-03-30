import django_filters
from django_filters.widgets import RangeWidget
from .models import Book, Author, CATEGORY_CHOICES, LANGUAGE_CHOICES, Item, STATUS_CHOICES

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='By book title'
    )
    category = django_filters.filters.ChoiceFilter(
        choices=CATEGORY_CHOICES,
        label='By category'
    )
    language = django_filters.filters.ChoiceFilter(
        choices=LANGUAGE_CHOICES,
        label='By language'
    )
    authors = django_filters.CharFilter(
        field_name='authors__surname',
        lookup_expr='icontains',
        label='By author surname'
    )
    publisher = django_filters.CharFilter(
        lookup_expr='icontains',
        label='By publisher'
    )
    year_of_publishing = django_filters.RangeFilter(
        label='Year of publishing (from - to)',
        widget=RangeWidget(
            attrs={
                'class': 'form-control form-inline col-3'
            }
        )
    )
    pages = django_filters.RangeFilter(
        label='Number of pages (range)',
        widget=RangeWidget(
            attrs={
                'class': 'form-control form-inline col-2'
            }
        )
    )

    class Meta:
        model = Book
        fields = ['title', 'authors', 'category', 'language',
                  'publisher', 'year_of_publishing', 'pages']
        ordering = ['-id']


class AuthorFilter(django_filters.FilterSet):
    surname = django_filters.CharFilter(
        lookup_expr='icontains',
        label='By surname'
    )

    class Meta:
        model = Author
        fields = ['surname']
        ordering = ['-id']


class ItemFilter(django_filters.FilterSet):
    inventory_number = django_filters.CharFilter(
        lookup_expr='icontains',
        label='By inventory number',
    )
    status = django_filters.filters.ChoiceFilter(
        choices=STATUS_CHOICES,
        label='By status'
    )
    borrower = django_filters.CharFilter(
        field_name='operator__last_name',
        lookup_expr='icontains',
        label='By borrower surname',
    )

    class Meta:
        model = Item
        fields = ('inventory_number', 'status', 'borrower',)
        ordering = ['-id']
