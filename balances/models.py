from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill



# Create your models here.
class Question(models.Model):

    def question_image_path(instance, filename):
        return f'balances/{instance.title}/{filename}'
    
    title = models.CharField(max_length=30)
    category = models.IntegerField(default='###')
    content1_users = models.ManyToManyField(settings.AUTH_USER_MODEL,)
    content1 = models.TextField()
    content2 = models.TextField()
    image1 =  ProcessedImageField(
        upload_to= question_image_path,
        processors=[ResizeToFill(500,500)],
        format='JPEG',
        options={'quality' : 100},
    )
    image2 =  ProcessedImageField(
        upload_to= question_image_path,
        processors=[ResizeToFill(500,500)],
        format='JPEG',
        options={'quality' : 100},
    )


class Result(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Question, on_delete=models.CASCADE )
    chosen_result = models.CharField(max_length=100)