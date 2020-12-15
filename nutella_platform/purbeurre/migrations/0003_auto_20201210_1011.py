# Generated by Django 3.1.4 on 2020-12-10 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purbeurre', '0002_auto_20201209_2302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users_pur_beurre',
            old_name='nom',
            new_name='inputNom',
        ),
        migrations.RenameField(
            model_name='users_pur_beurre',
            old_name='password_hash',
            new_name='inputPassword',
        ),
        migrations.RenameField(
            model_name='users_pur_beurre',
            old_name='phone',
            new_name='inputPhone',
        ),
        migrations.RenameField(
            model_name='users_pur_beurre',
            old_name='sex',
            new_name='inputSex',
        ),
        migrations.RenameField(
            model_name='users_pur_beurre',
            old_name='username',
            new_name='inputUsername',
        ),
        migrations.RenameField(
            model_name='users_pur_beurre',
            old_name='email',
            new_name='inputemail',
        ),
        migrations.RenameField(
            model_name='users_pur_beurre',
            old_name='prenom',
            new_name='inputprenom',
        ),
        migrations.AlterField(
            model_name='users_pur_beurre',
            name='is_admin',
            field=models.BooleanField(null=True),
        ),
    ]