# Generated by Django 4.1.7 on 2024-07-13 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userRegistration', '0005_account_description_account_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='description',
        ),
        migrations.RemoveField(
            model_name='account',
            name='type',
        ),
    ]
