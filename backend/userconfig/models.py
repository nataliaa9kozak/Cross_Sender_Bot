from django.db import models
from users.models import CustomUser


class UserConfig(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='configs')
    content = models.JSONField()
    social_media = models.CharField(unique=True, max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.social_media}'

    class Meta:
        ordering = ['-timestamp']
