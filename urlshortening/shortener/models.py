from django.db import models

# Create your models here.
class URL(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    original_url = models.URLField(null=False, blank=False)
    shortened_url = models.CharField(max_length=20, unique=True, null=False, blank=False)
    user_email = models.CharField(max_length=200, null=False, blank=False) # this is user identifier
    view_count = models.BigIntegerField(default=0, null=False, blank=False)