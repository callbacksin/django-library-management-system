from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django_filters.views import FilterView

from .filters import BookFilter, AuthorFilter, ItemFilter
from .forms import BookForm, BookInstanceForm, AuthorForm
from .models import Item, Book, Author


def checkout(request):
    return render(request, "checkout.html")


@user_passes_test(lambda u: u.is_superuser)
def admin_panel(request):
    return render(request, "operate.html")


class HomeViewFilter(FilterView):
    model = Book
    paginate_by = 10
    template_name = "home.html"
    filterset_class = BookFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = BookFilter(
            self.request.GET, queryset=self.get_queryset())
        query = self.request.GET.copy()
        if 'page' in query:
            del query['page']
        context['queries'] = query
        return context


class AuthorViewFilter(FilterView):
    model = Author
    paginate_by = 10
    template_name = "core_lib/authors.html"
    filterset_class = AuthorFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AuthorFilter(
            self.request.GET, queryset=self.get_queryset())
        query = self.request.GET.copy()
        if 'page' in query:
            del query['page']
        context['queries'] = query
        return context


class ItemViewFilter(FilterView):
    model = Item
    paginate_by = 10
    template_name = "core_lib/items.html"
    filterset_class = ItemFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ItemFilter(
            self.request.GET, queryset=self.get_queryset())
        query = self.request.GET.copy()
        if 'page' in query:
            del query['page']
        context['queries'] = query
        return context


class AdminHomeViewFilter(HomeViewFilter):
    template_name = "core_lib/books.html"
    paginate_by = 10


class HomeView(ListView):
    model = Book
    paginate_by = 10
    template_name = "home.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "core_lib/student_book_view.html"


class BookDetailView(DetailView):
    model = Book
    template_name = "core_lib/student_book_view.html"


class AdminBookDetailView(BookDetailView):
    template_name = "core_lib/concrete_book.html"


@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def create_book(request):
    if request.POST:
        book_form = BookForm(request.POST)
        if book_form.is_valid():
            book_form.save()
            book_title = book_form.cleaned_data.get('title')
            messages.success(request,
                             f'Book "{book_title}" created successfully')
            return redirect('core:books')
        else:
            messages.info(request,
                          'Please correct the errors')
    else:
        book_form = BookForm()
    return render(request, 'core_lib/create_book.html',
                  {'book_form': book_form, })


@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book_form = BookForm(request.POST, instance=book)
        if book_form.is_valid():
            book = book_form.save(commit=False)
            book.operator = request.user
            book.save()
            messages.success(request,
                             'Book updated successfully')
            return redirect('core:admin_book', pk=pk)
        else:
            messages.info(request,
                          'Please correct the errors')
    else:
        book_form = BookForm(instance=book)
    return render(request, 'core_lib/update_book.html',
                  {'book_form': book_form, })


@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def update_author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        author_form = AuthorForm(request.POST, instance=author)
        if author_form.is_valid():
            author_form.save()
            messages.success(request,
                             'Author updated successfully')
            return redirect('core:authors')
        else:
            messages.info(request,
                          'Please correct the errors')
    else:
        author_form = AuthorForm(instance=author)
    return render(request, 'core_lib/update_author.html',
                  {'author_form': author_form, })


@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def delete_book(request, pk):
    book = Book.objects.filter(pk=pk).first()
    title = book.title
    if request.method == 'POST':
        book.delete()
        messages.success(request,
                         f'Book "{title}" deleted successfully')
    else:
        messages.info(request,
                      'Please correct the errors')
    return redirect('core:books')


@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def create_book_instance(request, pk):
    if request.POST:
        instance_form = BookInstanceForm(request.POST)
        if instance_form.is_valid():
            inventory = instance_form.cleaned_data.get('inventory_number')
            book = Book.objects.filter(pk=pk).first()
            book_instance = Item(
                operator=request.user,
                inventory_number=inventory,
                book=book, )
            book_instance.save()
            book.total_quantity += 1
            book.free_quantity += 1
            book.save()
            title = book.title
            messages.success(
                request,
                f'''Book instance of "{title}" created successfully
                 with inventory number {inventory}''')
            return redirect('core:admin_book', pk=book.pk)
        else:
            messages.info(request, 'Please correct the errors')
    else:
        instance_form = BookInstanceForm()
    return render(request, 'core_lib/create_book_instance.html',
                  {'instance_form': instance_form, })


@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def delete_book_instance(request, pk):
    item = Item.objects.filter(pk=pk).first()
    inventory = item.inventory_number
    if request.method == 'POST':
        item.delete()
        item.book.free_quantity -= 1
        item.book.total_quantity -= 1
        item.book.save()
        messages.success(request,
                         f'Book instance with inventory number "{inventory}" deleted successfully')
    else:
        messages.info(request,
                      'Please correct the errors')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
