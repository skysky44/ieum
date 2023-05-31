from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
class User(AbstractUser):
    SEOUL = '서울특별시청'
    INCHEON = '인천광역시청'
    BUSAN = '부산광역시청'
    ULSAN = '울산광역시청'
    DAEGU = '대구광역시청'
    GWANGJU = '광주광역시청'
    DAEJEON = '대전광역시청'
    JEJU = '제주특별자치도청'
    GYEONGGI = '경기도청'
    GANGWON = '강원도청'
    CHUNGBUK = '충청북도청'
    CHUNGNAM = '충청남도청'
    JEONBUK = '전라북도청'
    JEONNAM = '전라남도청'
    GYEONGBUK = '경상북도청'
    GYEONGNAM = '경상남도청'    
    REGION_CHOICES = [
        (SEOUL, '서울특별시청'), (INCHEON, '인천광역시청'), (BUSAN, '부산광역시청'), (ULSAN, '울산광역시청'), (DAEGU, '대구광역시청'), (GWANGJU, '광주광역시청'), (DAEJEON, '대전광역시청'), (JEJU, '제주특별자치도청'), (GYEONGGI, '경기도청'), (GANGWON, '강원도청'), (CHUNGBUK, '충청북도청'), (CHUNGNAM, '충청남도청'), (JEONBUK, '전라북도청'), (JEONNAM, '전라남도청'), (GYEONGBUK, '경상북도청'),(GYEONGNAM, '경상남도청'),
    ]
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    birthday = models.DateField(null=True, blank=True)
    tags = models.CharField(max_length=100, default='태그')
    image = models.ImageField(blank=True, upload_to='')
    region = models.CharField(max_length=10, choices=REGION_CHOICES, default=SEOUL)
    score = models.IntegerField(default=100)
    taste = models.CharField(max_length=2, default='N')

    # SMALL = "특별함 보다 소소한 행복을 추구해요."
    # FUTURE = "미래보다는 매 순간 최선을 다하는 것이 더 중요해요."
    # lIKE = "내가 좋아하는 걸로 삶을 채워가고 싶어요."
    # FAST = "빠른 것보다 천천히 나아가는 것이 낫다고 생각해요."
    # HELP = "누군가에게 영감을 주는 삶을 살고 싶어요."
    # HOBBY = "관심있는 취미들을 깊게 더 나눠보고 싶어요."
    # VALUE = "경험을 통해 얻는 가치가 중요해요."
    # START = "결과보다는 시작하는 것이 더 가치 있다고 생각해요."
    # KIND = "선한 영향력을 가진 사람이 되고 싶어요."
    # SEPECIAL = "반복되는 일상을 특별하게 만들어 보고 싶어요."
    # PLAY = "함께 먹고 마시고 떠들며 놀고 싶어요!"
    # GOAL = "새로운 목표를 같이 달성해보고 싶어요."
    # GROWTH = "서로의 고민이나 생각을 나누며 함께 성장해보고 싶어요."
    # TOGETHER = "혼자 하기 두려웠던 것들을 함께 시작해 보고 싶어요."
    # ENJOYMAKE = "즐거운 삶은 스스로 만들어 나가는 것이라고 생각해요."
    # BALANCE = "일과 삶의 균형을 중요하게 생각해요."
    # CONTINUE = "지속 가능한 삶에 대해 중요하게 생각해요."
    # VARIOUSSPACE = "가보지 못했던 다양한 장소를 같이 가보고 싶어요."
    # NEW = "새로운 사람들과 함께 다채로운 경험을 쌓고 싶어요."
    # QUESTION = "스스로에게 끊임 없이 질문하는 삶을 지향해요."
    # LEARN = "늘 배우고 성장하는 것이 가장 큰 목표예요."
    # EXCAVATE = "몰랐던 취미나 관심사를 함께 발굴해나가 봐요!"
    
    # SENTENCE_CHOICES = [(SMALL, "특별함 보다 소소한 행복을 추구해요."),
    # (FUTURE, "미래보다는 매 순간 최선을 다하는 것이 더 중요해요."),
    # (lIKE, "내가 좋아하는 걸로 삶을 채워가고 싶어요."),
    # (FAST, "빠른 것보다 천천히 나아가는 것이 낫다고 생각해요."),
    # (HELP, "누군가에게 영감을 주는 삶을 살고 싶어요."),
    # (HOBBY, "관심있는 취미들을 깊게 더 나눠보고 싶어요."),
    # (VALUE, "경험을 통해 얻는 가치가 중요해요."),
    # (START, "결과보다는 시작하는 것이 더 가치 있다고 생각해요."),
    # (KIND, "선한 영향력을 가진 사람이 되고 싶어요."),
    # (SEPECIAL, "반복되는 일상을 특별하게 만들어 보고 싶어요."),
    # (PLAY, "함께 먹고 마시고 떠들며 놀고 싶어요!"),
    # (GOAL, "새로운 목표를 같이 달성해보고 싶어요."),
    # (GROWTH, "서로의 고민이나 생각을 나누며 함께 성장해보고 싶어요."),
    # (TOGETHER, "혼자 하기 두려웠던 것들을 함께 시작해 보고 싶어요."),
    # (ENJOYMAKE, "즐거운 삶은 스스로 만들어 나가는 것이라고 생각해요."),
    # (BALANCE, "일과 삶의 균형을 중요하게 생각해요."),
    # (CONTINUE, "지속 가능한 삶에 대해 중요하게 생각해요."),
    # (VARIOUSSPACE, "가보지 못했던 다양한 장소를 같이 가보고 싶어요."),
    # (NEW, "새로운 사람들과 함께 다채로운 경험을 쌓고 싶어요."),
    # (QUESTION, "스스로에게 끊임 없이 질문하는 삶을 지향해요."),
    # (LEARN, "늘 배우고 성장하는 것이 가장 큰 목표예요."),
    # (EXCAVATE, "몰랐던 취미나 관심사를 함께 발굴해나가 봐요!")]
    # my_sentence = models.CharField(max_length=100, choices=SENTENCE_CHOICES, blank=True, null=True)

    # reported = models.BooleanField(default=False)
    


class Track(models.Model):
    # id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    image_url = models.URLField()
    preview_url = models.URLField()
    is_selected = models.BooleanField(default=False)  # 선택 여부를 나타내는 필드

    def __str__(self):
        return self.title