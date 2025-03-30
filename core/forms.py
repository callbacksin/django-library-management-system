from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError

from .models import Author, Book, Item


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('surname', 'name',)


class BookInstanceForm(forms.Form):
    inventory_number = forms.CharField(
        label='Inventory number',
        max_length=20,
        help_text='Inventory numbers must be unique',
    )

    def clean_inventory_number(self):
        inventory = self.cleaned_data['inventory_number']
        if Item.objects.filter(inventory_number=inventory).exists():
            raise ValidationError('A book instance with this inventory number already exists')
        return inventory


class BookForm(forms.ModelForm):
    total_quantity = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=0
    )
    free_quantity = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=0
    )
    authors = forms.ModelMultipleChoiceField(
        label='Authors',
        queryset=Author.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url='author_autocomplete',
            attrs={
                'data-placeholder': 'Enter author\'s surname for auto search',
                'data-minimum-input-length': 0,
                'data-max-results': 10,
                'style': 'width:100%',
                'data-html': True,
            }),
        help_text='''You can select multiple authors for the book.
                     Start typing to let the system suggest options.
                     If the author is not listed, a new author will be automatically created.'''
    )

    class Meta:
        model = Book
        fields = ('title', 'authors', 'language', 'category',
                  'total_quantity', 'free_quantity', 'publisher',
                  'year_of_publishing', 'pages')
