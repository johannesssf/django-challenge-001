# Generated by Django 3.1.5 on 2021-06-08 14:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('picture', models.URLField(verbose_name='Picture')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100, verbose_name='Category')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('summary', models.CharField(max_length=300, verbose_name='Summary')),
                ('first_paragraph', models.CharField(max_length=300, verbose_name='First paragraph')),
                ('body', models.TextField(verbose_name='Body')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.author')),
            ],
        ),
    ]