from django.db import models


# Create your models here.
class URL(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    original_url = models.URLField(null=False, blank=False)
    shortened_url = models.CharField(max_length=20, unique=True, null=False, blank=False)
    user_email = models.CharField(max_length=200, null=False, blank=False)
    view_count = models.BigIntegerField(default=0, null=False, blank=False)

    class Meta:
        db_table = "urls"
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["user_email"]),
        ]

    def __str__(self) -> str:
        return f"URL<{self.id} | {self.original_url} | {self.shortened_url} | {self.user_email} | {self.view_count}>"
