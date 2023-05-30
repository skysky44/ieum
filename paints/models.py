from django.db import models
from django.conf import settings

class Paint(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='paints/')
    created_at = models.DateTimeField(auto_now = True)