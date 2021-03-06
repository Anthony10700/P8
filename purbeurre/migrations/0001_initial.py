# Generated by Django 3.1.4 on 2020-12-16 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('url', models.URLField(unique=True)),
                ('nb_of_products', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('countries', models.CharField(max_length=200, null=True)),
                ('id_openfoodfacts', models.CharField(max_length=200, unique=True)),
                ('url', models.URLField(unique=True)),
                ('image_url', models.URLField(unique=True)),
                ('store', models.CharField(max_length=200, null=True)),
                ('nutriscore_grade', models.CharField(max_length=1)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purbeurre.categories')),
            ],
        ),
        migrations.CreateModel(
            name='Products_save',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.ManyToManyField(to='purbeurre.Product')),
                ('user_id', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
