# Generated by Django 3.2.18 on 2023-06-08 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reported',
            field=models.BooleanField(default=False),
        ),
    ]
