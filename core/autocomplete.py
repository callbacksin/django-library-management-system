from dal import autocomplete
from django.contrib.auth.decorators import login_required

from .models import Author, Book, Item


class AuthorAutocomplete(autocomplete.Select2QuerySetView):

    def get_result_label(self, item):
        return f'{item.surname} {item.name}'

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Author.objects.none()

        qs = Author.objects.all()

        if self.q:
            qs = qs.filter(surname__istartswith=self.q)

        return qs


class BookAutocomplete(autocomplete.Select2QuerySetView):

    def get_result_label(self, item):
        return f'{item.title}'

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Book.objects.none()

        qs = Book.objects.all()

        if self.q:
            qs = qs.filter(title__istartswith=self.q)

        return qs


class ItemAutocomplete(autocomplete.Select2QuerySetView):

    def get_result_label(self, item):
        return f'{item.inventory_number}'

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Item.objects.none()

        qs = Item.objects.all()

        if self.q:
            qs = qs.filter(inventory_number__istartswith=self.q)

        return qs