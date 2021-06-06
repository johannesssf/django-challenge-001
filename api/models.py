import uuid

from django.db import models


class Author(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Name", max_length=150)
    picture = models.URLField("Picture")
