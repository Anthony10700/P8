# Generated by Django 3.1.4 on 2021-02-08 21:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purbeurre', '0008_auto_20210108_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='like_disklike_products',
            field=models.ManyToManyField(related_name='like_disklike_products', to=settings.AUTH_USER_MODEL),
        ),
    ]
