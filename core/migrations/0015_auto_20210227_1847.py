# Generated by Django 2.2.13 on 2021-02-27 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20210227_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('F', 'Есть в наличии'), ('A', 'Отсутствует')], max_length=1),
        ),
    ]
