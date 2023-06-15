# Generated by Django 3.2.18 on 2023-06-14 18:55

import balances.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('content1', models.TextField()),
                ('content2', models.TextField()),
                ('word1', models.CharField(blank=True, max_length=1000, null=True)),
                ('word2', models.CharField(blank=True, max_length=1000, null=True)),
                ('image1', imagekit.models.fields.ProcessedImageField(upload_to=balances.models.Question.question_image_path)),
                ('image2', imagekit.models.fields.ProcessedImageField(upload_to=balances.models.Question.question_image_path)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chosen_result', models.JSONField(default=list)),
                ('word', models.JSONField(default=list)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
