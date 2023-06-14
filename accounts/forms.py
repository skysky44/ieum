from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm,  PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import User
from balances.models import Result
import datetime

SENTENCE_CHOICES = [('특별함 보다 소소한 행복을 추구해요.', "특별함 보다 소소한 행복을 추구해요."),
        ('미래보다는 매 순간 최선을 다하는 것이 더 중요해요.', "미래보다는 매 순간 최선을 다하는 것이 더 중요해요."),
        ('내가 좋아하는 걸로 삶을 채워가고 싶어요.', "내가 좋아하는 걸로 삶을 채워가고 싶어요."),
        ('빠른 것보다 천천히 나아가는 것이 낫다고 생각해요.', "빠른 것보다 천천히 나아가는 것이 낫다고 생각해요."),
        ('누군가에게 영감을 주는 삶을 살고 싶어요.', "누군가에게 영감을 주는 삶을 살고 싶어요."),
        ('관심있는 취미들을 깊게 더 나눠보고 싶어요.', "관심있는 취미들을 깊게 더 나눠보고 싶어요."),
        ('경험을 통해 얻는 가치가 중요해요.', "경험을 통해 얻는 가치가 중요해요."),
        ('결과보다는 시작하는 것이 더 가치 있다고 생각해요.', "결과보다는 시작하는 것이 더 가치 있다고 생각해요."),
        ('선한 영향력을 가진 사람이 되고 싶어요.', "선한 영향력을 가진 사람이 되고 싶어요."),
        ('반복되는 일상을 특별하게 만들어 보고 싶어요.', "반복되는 일상을 특별하게 만들어 보고 싶어요."),
        ('함께 먹고 마시고 떠들며 놀고 싶어요!', "함께 먹고 마시고 떠들며 놀고 싶어요!"),
        ('새로운 목표를 같이 달성해보고 싶어요.', "새로운 목표를 같이 달성해보고 싶어요."),
        ('서로의 고민이나 생각을 나누며 함께 성장해보고 싶어요.', "서로의 고민이나 생각을 나누며 함께 성장해보고 싶어요."),
        ('혼자 하기 두려웠던 것들을 함께 시작해 보고 싶어요.', "혼자 하기 두려웠던 것들을 함께 시작해 보고 싶어요."),
        ('즐거운 삶은 스스로 만들어 나가는 것이라고 생각해요.', "즐거운 삶은 스스로 만들어 나가는 것이라고 생각해요."),
        ('일과 삶의 균형을 중요하게 생각해요.', "일과 삶의 균형을 중요하게 생각해요."),
        ('지속 가능한 삶에 대해 중요하게 생각해요.', "지속 가능한 삶에 대해 중요하게 생각해요."),
        ('가보지 못했던 다양한 장소를 같이 가보고 싶어요.', "가보지 못했던 다양한 장소를 같이 가보고 싶어요."),
        ('새로운 사람들과 함께 다채로운 경험을 쌓고 싶어요.', "새로운 사람들과 함께 다채로운 경험을 쌓고 싶어요."),
        ('스스로에게 끊임 없이 질문하는 삶을 지향해요.', "스스로에게 끊임 없이 질문하는 삶을 지향해요."),
        ('늘 배우고 성장하는 것이 가장 큰 목표예요.', "늘 배우고 성장하는 것이 가장 큰 목표예요."),
        ('몰랐던 취미나 관심사를 함께 발굴해나가 봐요!', "몰랐던 취미나 관심사를 함께 발굴해나가 봐요!")]

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="아이디",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',

            }
        ),
    )

    first_name = forms.CharField(
        label="이름",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',

            }

        ),
    )
    birthday = forms.DateField(
        initial=datetime.date(2000, 1, 1),
        label="생일",
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',

            }
        ),
    )
    email = forms.EmailField(
        label="이메일",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',


            }
        ),
    )
    image = forms.ImageField(
        label='프로필 이미지',
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',

            }
        ),
    )
    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',

            }
        ),
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',

            }
        ),
    )

    region = forms.ChoiceField(
        choices=User.REGION_CHOICES,
        label='지역',
        widget=forms.Select(
            attrs={
                'class': 'form-control',

            }
        ),
    )

    privacy = forms.BooleanField(
        label="지역 공개 여부",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        ),
    )

    introductions = forms.MultipleChoiceField(
        choices=SENTENCE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    password = None

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'birthday', 'email',
                'image', 'password1', 'password2', 'region', 'privacy', 'introductions')


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(
        label=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'style': 'width:350px; border:none;',
            }
        ),
    )
    first_name = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'style': 'width:350px; border:none;',
            }
        ),
    )
    region = forms.ChoiceField(
        choices=User.REGION_CHOICES,
        label='지역',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'style': 'width:350px; border:none;',
            }
        ),
    )

    privacy = forms.BooleanField(
        label="지역 공개 여부",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        ),
    )

    birthday = forms.DateField(
        initial=datetime.date(2000, 1, 1),
        label=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'style': 'width:350px; border:none;',
            }
        ),
    )

    image = forms.ImageField(
        label=False,
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'style': 'width:350px;',
            }
        ),
    )

    introductions = forms.MultipleChoiceField(
        choices=SENTENCE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    password = None

    introductions = forms.MultipleChoiceField(
        choices=SENTENCE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta(UserChangeForm.Meta):
        model = get_user_model()

        fields = ('email', 'first_name', 'region', 'privacy', 'birthday', 'image', 'introductions')



class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '아이디',
            }
        ),
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호',
            }
        ),
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '기존 비밀번호',

            }
        ),
    )
    new_password1 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '새 비밀번호',
            }
        ),
        help_text='',
    )
    new_password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '새 비밀번호(확인)',
            }
        ),
        help_text='',
    )

class ResultForm(forms.ModelForm):
    words = forms.MultipleChoiceField(
        label=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ResultForm, self).__init__(*args, **kwargs)
        result_queryset = Result.objects.filter(user=user)
        choices = []
        for result in result_queryset:
            for selected_words in result.word.values():
                for word in selected_words:
                    # Create a tuple with the key-value pair for the choice label and value
                    choice = (word, word)
                    choices.append(choice)
        self.fields['words'].choices = choices

    class Meta:
        model = get_user_model()
        fields = ('words',)