from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from core.autocomplete import AuthorAutocomplete, BookAutocomplete, ItemAutocomplete
from core.models import Author
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls', namespace='core')),
    path('lib-users/', include('lib_users.urls')),
    path('order-process/', include('order_process.urls')),
    url(r'^author-autocomplete/$',
        AuthorAutocomplete.as_view(model=Author, create_field='surname'),
        name="author_autocomplete"),
    url(r'^book-autocomplete/$',
        BookAutocomplete.as_view(),
        name="book_autocomplete"),
    url(r'^item-autocomplete/$',
        ItemAutocomplete.as_view(),
        name="item_autocomplete"),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()


