from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    """
    Base model for basic fields that most Models will use.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class UserProfile(BaseModel):
    """
    Basic profile to attach to user accounts. Used for storing
    information and preferences for a user that are not a part of
    the user/auth model.
    """
    owner = models.ForeignKey(User)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)


class Snippet(BaseModel):
    """
    Model for a single Snippet instance.
    """
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
    color = models.CharField(max_length=20,
                             default="white",
                             choices=COLOR_CHOICES)
    starred = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'url')


class Tag(BaseModel):
    """
    A basic tag model to allow a user to tag Snippets.

    Note that the Tag model itself does not contain any references to
    its associated Snippet(s). This is done in the TagSnippetRelation model.
    """
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('owner', 'title')


class TagSnippetRelation(BaseModel):
    """
    A relation tying a Tag to a Snippet.
    """
    owner = models.ForeignKey(User)
    _tag = models.ForeignKey(Tag)
    _snippet = models.ForeignKey(Snippet, related_name="tags")

    def __str__(self):
        return str(self._tag)

    class Meta:
        unique_together = ('owner', '_tag', '_snippet')
