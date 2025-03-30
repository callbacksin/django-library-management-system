from django.contrib import admin

from .models import Item, Book, Author, ItemHistory
from .forms import BookForm

admin.site.register(Item)
admin.site.register(Author)
admin.site.register(ItemHistory)


class BookAdmin(admin.ModelAdmin):
    form = BookForm


admin.site.register(Book, BookAdmin)
