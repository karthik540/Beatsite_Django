# Generated by Django 2.2 on 2019-06-22 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0004_customuser_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='bio',
        ),
    ]
