# Generated by Django 3.2.18 on 2023-06-14 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balances', '0002_auto_20230615_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='word1',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='word2',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]