from django.conf import settings
from django.db import models
from django.shortcuts import reverse

CATERGORY_CHOICES = (
    ('S', 'Методические указания'),
    ('H', 'Художественная литература'),
    ('T', 'Техническая литература'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)

LANGUAGE_CHOICES = (
    ('E', 'Английский'),
    ('R', 'Русский'),
    ('B', 'Белорусский'),
)

STATUS_CHOICES = (
    ('F', 'Есть в наличии'),
    ('A', 'Отсутствует'),
)


class Author(models.Model):
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.surname + " " + self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    # description = models.TextField()
    authors = models.ManyToManyField(Author)
    language = models.CharField(choices=LANGUAGE_CHOICES,
                                max_length=1,
                                default='R')
    category = models.CharField(choices=CATERGORY_CHOICES,
                                max_length=2)
    label = models.CharField(choices=LABEL_CHOICES,
                             max_length=1)
    # qr-code

    def __str__(self):
        return self.title + " (" + str(self.id) + ")"

    def get_absolute_url(self):
        return reverse("core:book", kwargs={
            "pk": self.id
        })

    def get_total_count(self):
        return Item.objects.filter(book=self.id).count()

    def get_free_count(self):
        return Item.objects.filter(book=self.id, status='F').count()


class Item(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=1,
                              default='F',
                              )
    inventory_number = models.CharField(max_length=20,
                                        unique=True)

    def __str__(self):
        return self.inventory_number + " - " + self.book.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            "slug": self.id
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            "slug": self.id
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            "slug": self.id
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item,
                             on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    # def get_total(self):
    #     total = 0
    #     for order_item in self.items.all():
    #         total += order_item.get_final_price()
    #     return total
