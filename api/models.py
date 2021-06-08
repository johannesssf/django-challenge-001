import uuid

from django.db import models


class Author(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Name", max_length=150)
    picture = models.URLField("Picture")


class Article(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    category = models.CharField("Category", max_length=100)
    title = models.CharField("Title", max_length=200)
    summary = models.CharField("Summary", max_length=300)
    first_paragraph = models.CharField("First paragraph", max_length=300)
    body = models.TextField("Body")
