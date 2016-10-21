from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Snippet(BaseModel):
    COLOR_CHOICES = (
        ('white', 'white'),
        ('red', 'red'),
        ('green', 'green'),
        ('blue', 'blue'),
        ('yellow', 'yellow'),
        ('orange', 'orange'),
        ('teal', 'teal'),
        ('gray', 'gray')
    )

    owner = models.ForeignKey(User)
    title = models.CharField(max_length=255, default="Untitled Snippet")
    url = models.URLField(blank=False)
    color = models.CharField(max_length=20, default="white", choices=COLOR_CHOICES)
    starred = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
