from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils import timezone
from datetime import timedelta,datetime
from taggit.managers import TaggableManager
# from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.fields import RichTextUploadingField
import re

def extract_image_urls(content):
    pattern = r'<img.*?src=["\'](.*?)["\'].*?>'
    image_urls = re.findall(pattern, content)
    return image_urls

# class ListField(models.TextField):
#     def from_db_value(self, value, expression, connection):
#         if value is not None:
#             return value.split(", ")
#         return []

#     def to_python(self, value):
#         if isinstance(value, list):
#             return value
#         if value is not None:
#             return value.split(", ")
#         return []

#     def get_prep_value(self, value):
#         return ', '.join(value)

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    # content = RichTextUploadingField(blank=True,null=True)
    content = RichTextUploadingField()
    # content = CKEditorField('Content', config_name='extends')
    category = models.CharField(max_length=20)
    address = models.CharField(max_length=20, blank=True)
    place_name = models.CharField(max_length=50, blank=True) 
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now = True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_post')
    tags = TaggableManager(blank=True)
    report = models.BooleanField('신고', default=False)
    # image_urls = ListField(blank=True, null=True)
    image_urls = models.TextField(blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    
    # def save(self, *args, **kwargs):
    #     self.image_urls = extract_image_urls(self.content)
    #     super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        # content에서 이미지 URL 추출하여 image_urls 필드에 저장
        self.image_urls = ', '.join(extract_image_urls(self.content))
        super().save(*args, **kwargs)

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
    report = models.BooleanField('신고', default=False)

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

class PostReport(models.Model):
    SPAM = '스팸홍보/도배글입니다.'
    DISAGREEABLE = '음란물/불쾌한 표현을 포함하고 있습니다.'
    LIE = '해로운 허위 정보를 포함하고 있습니다.'
    ILLEGALITY = '불법정보를 포함하고 있습니다.'
    PRIVACY = '개인정보 노출 게시물입니다.'
    OTHERS = '기타'
    TITLE_CHOICES = [
        (SPAM, '스팸홍보/도배글입니다.'), (DISAGREEABLE, '음란물/불쾌한 표현을 포함하고 있습니다.'), 
        (LIE, '해로운 허위 정보를 포함하고 있습니다.'), (ILLEGALITY, '불법정보를 포함하고 있습니다.'),
        (PRIVACY, '개인정보 노출 게시물입니다.'), (OTHERS, '기타'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_report')
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now = True)


class CommentReport(models.Model):
    SPAM = '스팸홍보/도배글입니다.'
    DISAGREEABLE = '음란물/불쾌한 표현을 포함하고 있습니다.'
    LIE = '해로운 허위 정보를 포함하고 있습니다.'
    ILLEGALITY = '불법정보를 포함하고 있습니다.'
    PRIVACY = '개인정보 노출 게시물입니다.'
    OTHERS = '기타'
    TITLE_CHOICES = [
        (SPAM, '스팸홍보/도배글입니다.'), (DISAGREEABLE, '음란물/불쾌한 표현을 포함하고 있습니다.'), 
        (LIE, '해로운 허위 정보를 포함하고 있습니다.'), (ILLEGALITY, '불법정보를 포함하고 있습니다.'),
        (PRIVACY, '개인정보 노출 게시물입니다.'), (OTHERS, '기타'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_report')
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
    
class Fortune(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)