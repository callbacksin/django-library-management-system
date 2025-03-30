from core.mixins import IsSuperUserMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView

from core.models import Item, Book
from order_process.models import Order, OrderBook


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                "object": order
            }
            return render(self.request, 'order_processing/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You have no active order")
            return redirect("/")


class UserOrderListView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user_orders = Order.objects.filter(user=self.request.user)
        if user_orders:
            context = {
                "object": user_orders
            }
            return render(self.request, 'order_processing/user_orders.html', context)
        else:
            messages.info(self.request, "You have no orders")
            return redirect("/")


class UserOrderDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        try:
            user_order = Order.objects.get(pk=pk, user=self.request.user)
            context = {
                "object": user_order
            }
            return render(self.request, 'order_processing/user_order.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "Something went wrong")
            return redirect("/")


class OrderListView(IsSuperUserMixin, ListView):
    paginate_by = 10
    queryset = Order.objects.filter(ordered=True, completed=False)
    template_name = 'order_processing/orders.html'


class CompletedOrderListView(IsSuperUserMixin, ListView):
    paginate_by = 10
    queryset = Order.objects.filter(completed=True)
    template_name = 'order_processing/completed_orders.html'


class OrderDetailView(IsSuperUserMixin, DetailView):
    model = Order
    template_name = 'order_processing/order.html'


class CompletedOrderDetailView(IsSuperUserMixin, DetailView):
    model = Order
    template_name = 'order_processing/completed_order.html'


@login_required
def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    order_book, created = OrderBook.objects.get_or_create(
        book=book,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.books.filter(book__pk=book.pk).exists():
            messages.info(request, "This book is already in the cart")
        else:
            messages.info(request, "The book has been added to the cart")
            order.books.add(order_book)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
                                     ordered_date=ordered_date)
        order.books.add(order_book)
        messages.info(request, "The book has been added to the cart")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_from_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order book is in the order
        if order.books.filter(book__pk=book.pk).exists():
            order_item = OrderBook.objects.filter(
                book=book,
                user=request.user,
                ordered=False
            )[0]
            order.books.remove(order_item)
            messages.info(request, "The book has been removed from the cart")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            # add a message saying the user doesn't have the order item
            messages.info(
                request,
                "This book was not in the cart")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        # add a message saying the user doesn't have an order
        messages.info(
            request,
            "You have no active order")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@transaction.atomic
def send_order(request):
    order = Order.objects.get(user=request.user, ordered=False)
    order_books = order.books.all()
    order_books.update(ordered=True)
    for book in order_books:
        book.save()

    order.ordered = True
    order.save()
    messages.success(request,
                     'The order has been sent to the library staff')
    return redirect('core:home')


@user_passes_test(lambda u: u.is_superuser)
def set_orderbook_unavailable(request, pk):
    orderbook = get_object_or_404(OrderBook, pk=pk)
    orderbook.is_in_library = False
    orderbook.save()
    messages.info(request,
                  'Set: The book instance is unavailable')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda u: u.is_superuser)
def set_orderbook_available(request, pk):
    orderbook = get_object_or_404(OrderBook, pk=pk)
    orderbook.is_in_library = True
    orderbook.save()
    messages.info(request,
                  '''Set: The book instance is available in the library
                  and will be added to the order''')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda u: u.is_superuser)
def complete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.completed = True
    order.comment = request.GET.get('comment')
    order.save()
    return redirect('orders')
