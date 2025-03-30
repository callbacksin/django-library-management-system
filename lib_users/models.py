from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from core.models import Item, ItemHistory


class Group(models.Model):
    group_name = models.CharField(
        max_length=6,
        verbose_name='Group')

    def __str__(self):
        return self.group_name


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Username')
    academy_group = models.ForeignKey(
        Group,
        on_delete=models.DO_NOTHING,
        verbose_name='Group')
    patronymic = models.CharField(
        max_length=50,
        verbose_name='Patronymic',
        default='Igorevich'
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Date of Birth')

    def __str__(self):
        return self.academy_group.group_name + " " + self.user.last_name + " " + self.user.first_name

    def get_absolute_url(self):
        return reverse("concrete", kwargs={
            "pk": self.user.id
        })

    def get_related_book_instances(self):
        return Item.objects.filter(borrower=self.user.id)

    def get_related_history(self):
        return ItemHistory.objects.filter(borrower=self.user.id)
