from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils import timezone
from datetime import timedelta,datetime
from taggit.managers import TaggableManager
# from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    # content = RichTextUploadingField(blank=True,null=True)
    content = RichTextUploadingField()
    # content = CKEditorField('Content', config_name='extends')
    category = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now = True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_post')
    tags = TaggableManager(blank=True)

    @property
    def created_time(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.created_at.strftime('%Y-%m-%d')



class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now = True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comment' )
    category = models.CharField(max_length=20)

    @property
    def created_time(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.created_at.strftime('%Y-%m-%d')

class CommentReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comments')
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now = True)


class PostTrack(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    preview_url = models.URLField()
    is_selected = models.BooleanField(default=False)
    image = models.ImageField(upload_to='post_track_images')

    def __str__(self):
        return self.title