# Generated by Django 4.1.3 on 2022-12-02 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_employee',
            field=models.BooleanField(default=False),
        ),
    ]
