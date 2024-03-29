from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    SEOUL = '서울특별시'
    INCHEON = '인천광역시'
    BUSAN = '부산광역시'
    ULSAN = '울산광역시'
    DAEGU = '대구광역시'
    GWANGJU = '광주광역시'
    DAEJEON = '대전광역시'
    JEJU = '제주특별자치도'
    GYEONGGI = '경기도'
    GANGWON = '강원도'
    CHUNGBUK = '충청북도'
    CHUNGNAM = '충청남도'
    JEONBUK = '전라북도'
    JEONNAM = '전라남도'
    GYEONGBUK = '경상북도'
    GYEONGNAM = '경상남도'    
    REGION_CHOICES = [
        (SEOUL, '서울특별시'), (INCHEON, '인천광역시'), (BUSAN, '부산광역시'), (ULSAN, '울산광역시'), (DAEGU, '대구광역시'), (GWANGJU, '광주광역시'), (DAEJEON, '대전광역시'), (JEJU, '제주특별자치도'), (GYEONGGI, '경기도'), (GANGWON, '강원도'), (CHUNGBUK, '충청북도'), (CHUNGNAM, '충청남도'), (JEONBUK, '전라북도'), (JEONNAM, '전라남도'), (GYEONGBUK, '경상북도'),(GYEONGNAM, '경상남도'),
    ]
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(blank=True, upload_to='')
    region = models.CharField(max_length=10, choices=REGION_CHOICES, default=SEOUL)
    score = models.IntegerField(default=140)
    taste = models.CharField(max_length=2, default='N')
    privacy = models.BooleanField(default=False)
    introductions = models.CharField(max_length=255)
    reported = models.BooleanField(default=False)
    words = models.JSONField(null=True, blank=True)


class Track(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    preview_url = models.URLField()
    is_selected = models.BooleanField(default=False)
    image = models.ImageField(upload_to='track_images')

    def __str__(self):
        return self.title
