from django.conf import settings
from django.db import models

from core.models import Book


class OrderBook(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='User')
    ordered = models.BooleanField(
        default=False,
        verbose_name='Order sent')
    book = models.ForeignKey(
        Book,
        on_delete=models.DO_NOTHING,
        verbose_name='Book instance')
    is_in_library = models.BooleanField(
        default=False,
        verbose_name='Availability of book instance when ordering'
    )

    class Meta:
        verbose_name = 'Book in order'
        verbose_name_plural = '4 DEBUG - Books in order'

    def __str__(self):
        return f"{self.book.title}"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='User')
    books = models.ManyToManyField(
        OrderBook,
        verbose_name='Books in order')
    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Order creation date')
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(
        default=False,
        verbose_name='Order sent'
    )
    completed = models.BooleanField(
        default=False,
        verbose_name='Order completed'
    )
    comment = models.CharField(
        null=True,
        blank=True,
        verbose_name='Library staff comment',
        max_length=144
    )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = '5 DEBUG - Orders'

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}'
