from django import forms
from .models import Post, Comment, CommentReport
from taggit.forms import TagField, TagWidget

category_choices = (
    ('모임', '모임'),
    ('익명', '익명'),
)


class PostForm(forms.ModelForm):
    category = forms.ChoiceField(
        label='카테고리',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder' : '분류',
            }
        ),
        choices=category_choices,
    )
    widgets = {
            'tags':TagWidget(
                attrs={
                    'class': 'form-control', 
                    'placeholder': '콤마로 구분하여 입력해주세요',
                }
            ),        
        }
    help_texts = {
            'tags': '콤마로 구분하여 입력해주세요',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].label = '태그'

    class Meta:
        model = Post
        fields = ('title', 'content', 'category', 'address', 'tags')

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '제목을 입력해주세요',
                }
            ),

            # 'category': forms.ChoiceField(
            #     attrs={
            #         'class': 'form-control',
            #         'placeholder': '분류',
            #     },
            #     choices=category_choices,
            # ),
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '주소',
                }
            ),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields["content"].required = False
        self.fields['content'].label = '내용'
        self.fields['address'].label = '주소'
        # self.fields['created_at'].label = '생성일'
        # self.fields['updated_at'].label = '수정일'
        self.fields['category'].label = '분류'


# class PostImageForm(forms.ModelForm):
#     image = forms.ImageField(
#         widget=forms.ClearableFileInput(
#             attrs={
#                 'multiple': True,
#                 'class': 'd-none',
#             },
#         ),
#         required=False,
#     )




class CommentForm(forms.ModelForm):
    content = forms.CharField(
        max_length=200,
        label='내용',
        widget=forms.Textarea(
            attrs={
                'placeholder': '내용을 입력해주세요.',
            }
        )
    )

    class Meta:
        model = Comment
        fields = (
            "content",
        )
