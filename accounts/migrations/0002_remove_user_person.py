# Generated by Django 5.0.1 on 2024-01-29 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='person',
        ),
    ]
