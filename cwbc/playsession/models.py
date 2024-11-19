import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    division = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(11)])
    secondary_division = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(11)],
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['name']


class PlaySession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    created = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()

    class Meta:
        ordering = ['created']
        get_latest_by = 'created'
