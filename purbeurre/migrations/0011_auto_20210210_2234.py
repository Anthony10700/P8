# Generated by Django 3.1.4 on 2021-02-10 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purbeurre', '0010_auto_20210208_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='dislike_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='like_count',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
