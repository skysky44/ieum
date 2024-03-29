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

    def clean_introductions(self):
        selected_choices = self.cleaned_data.get('introductions')
        if selected_choices and len(selected_choices) > 3:
            raise forms.ValidationError('Please select 3 choices or fewer.')
        return selected_choices

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

# words 라는 필드에 밸런스 게임을 통해서 얻은 단어 값(DB에 각 질문을 통해 얻은 단어들)으로 만들기 때문에 사용자 메서드 정의
class ResultForm(forms.ModelForm):
    # 'words' 필드 정의 여러 선택지를 가질 수 있도록 MultipleChoiceField 사용
    words = forms.MultipleChoiceField(
        label=False,
        widget=forms.CheckboxSelectMultiple, # 체크박스로 선택할 수 있도록 위젯 설정
    )
    # 생성자 메서드 재정의
    def __init__(self, *args, **kwargs):
        # 'user' 매개변수를 꺼내고, 나머지 매개변수를 부모 클래스의 생성자로 전달
        user = kwargs.pop('user')
        super(ResultForm, self).__init__(*args, **kwargs)

        # 현재 사용자에 해당하는 Result 객체들을 가져옴
        result_queryset = Result.objects.filter(user=user)
        # 선택지를 저장할 리스트 초기화
        choices = []

        # 각 Result 객체의 'word' 필드에서 선택한 단어들을 가져와서 choices 리스트에 추가
        for result in result_queryset:
            for selected_words in result.word.values():
                for word in selected_words:
                    choice = (word, word)
                    choices.append(choice)
        # 'words' 필드의 선택지(choices)를 설정
        self.fields['words'].choices = choices

    class Meta:
        model = get_user_model() # 현재 사용자 모델을 가져옴
        fields = ('words',) # 폼에 포함할 필드를 지정
