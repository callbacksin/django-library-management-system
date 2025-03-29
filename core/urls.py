from django.urls import path

from .views import (
    ItemDetailView,
    checkout,
    BookDetailView,
    HomeViewFilter,
    admin_panel,
    create_book,
    create_book_instance,
    AdminHomeViewFilter,
    update_book,
    delete_book,
    AdminBookDetailView,
    delete_book_instance,
    update_author,
    AuthorViewFilter,
    ItemViewFilter,
)

app_name = 'core'

urlpatterns = [
    path('', HomeViewFilter.as_view(), name='home'),
    path('operate/', admin_panel, name='operate'),
    path('books/', AdminHomeViewFilter.as_view(), name='books'),
    path('checkout/', checkout, name='checkout'),
    path('product/<pk>', ItemDetailView.as_view(), name='product'),
    path('book/<pk>', BookDetailView.as_view(), name='book'),
    path('create-book/', create_book, name='create_book'),
    path('update-book/<pk>', update_book, name='update_book'),
    path('delete-book/<pk>', delete_book, name='delete_book'),
    path('book-admin-view/<pk>', AdminBookDetailView.as_view(), name='admin_book'),
    path('create-item/<pk>', create_book_instance, name='create_item'),
    path('delete-item/<pk>', delete_book_instance, name='delete_item'),
    path('update-author/<pk>', update_author, name='update_author'),
    path('authors/', AuthorViewFilter.as_view(), name='authors'),
    path('items/', ItemViewFilter.as_view(), name='items'),
]
