from datetime import date
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

# All Choices structures are defined here

CATEGORY_CHOICES = (
    ('S', 'Methodological Guidelines'),
    ('H', 'Fiction'),
    ('T', 'Technical Literature'),
    ('P', 'Philosophy'),
    ('S', 'Science'),
    ('B', 'Biography'),
    ('M', 'Mystery & Thriller'),
    ('F', 'Fantasy'),
)

LANGUAGE_CHOICES = (
    ('E', 'English'),
    ('R', 'Russian'),
    ('B', 'Belarusian'),
    ('F', 'French'),
    ('G', 'German'),
    ('S', 'Spanish'),
    ('C', 'Chinese'),
)

STATUS_CHOICES = (
    ('F', 'Available'),
    ('A', 'Unavailable'),
    ('H', 'Historical'),
)

# Entity section where concrete models are defined

class Author(models.Model):
    surname = models.CharField(
        max_length=50,
        verbose_name='Surname')
    name = models.CharField(
        max_length=50,
        verbose_name='First Name')

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = '1 - Authors'

    def __str__(self):
        return self.surname + " " + self.name


class Book(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Book Title')
    authors = models.ManyToManyField(
        'Author',
        verbose_name='Authors')
    language = models.CharField(
        choices=LANGUAGE_CHOICES,
        max_length=1,
        default='R',
        verbose_name='Language')
    category = models.CharField(
        choices=CATEGORY_CHOICES,
        max_length=2,
        verbose_name='Category')
    total_quantity = models.IntegerField(
        default=0,
        verbose_name='Total Copies')
    free_quantity = models.IntegerField(
        default=0,
        verbose_name='Available Copies in Library')
    publisher = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Publisher',
    )
    year_of_publishing = models.PositiveSmallIntegerField(
        verbose_name='Year of Publishing',
        null=True,
        blank=True,
    )
    pages = models.PositiveSmallIntegerField(
        verbose_name='Number of Pages',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = '2 - Books'

    def __str__(self):
        return self.title

    def get_user_absolute_url(self):
        return reverse("core:book", kwargs={
            "pk": self.id
        })

    def get_admin_absolute_url(self):
        return reverse("core:admin_book", kwargs={
            "pk": self.id
        })

    def get_related_items(self):
        return Item.objects.filter(book=self.id)

    def get_item_history(self):
        return ItemHistory.objects.filter(book=self.id)

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            "pk": self.id
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            "pk": self.id
        })


class AbstractItem(models.Model):
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        verbose_name='Operator',
        related_name="%(app_label)s_%(class)s_related1",
        related_query_name="%(app_label)s_%(class)ss1",)
    inventory_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Inventory Number')
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name='Book')
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=1,
        default='F',
        verbose_name='Status')
    due_back = models.DateField(
        null=True,
        blank=True,
        verbose_name='Return Date')
    borrower = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Borrower',
        related_name="%(app_label)s_%(class)s_related2",
        related_query_name="%(app_label)s_%(class)ss2",)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        abstract = True
        verbose_name = 'Book Instance'
        verbose_name_plural = '3 - Book Instances'

    def __str__(self):
        return f'Inventory: {self.inventory_number} - Book: {self.book.title}'

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            "slug": self.id
        })


class Item(AbstractItem):
    qr_code = models.CharField(
        max_length=200,
        verbose_name='QR Code',
        null=True,
        blank=True,
    )
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)


class ItemHistory(AbstractItem):
    inventory_number = models.CharField(
        max_length=20,
        verbose_name='Inventory Number')
    item = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        related_name='item_history')

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Instance History'
        verbose_name_plural = '6 - Instance History'
