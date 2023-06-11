from django import forms
from .models import Post, Comment, PostReport, CommentReport
from taggit.forms import TagField, TagWidget
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='default'))
    category = forms.ChoiceField(
        label='카테고리',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder' : '분류',
                'style': 'width:400px;'
            }
        )
    )
    widgets = {
            'tags':TagWidget(
                attrs={
                    'class': 'form-control', 
                    'placeholder': '콤마로 구분하여 입력해주세요',
                    'style': 'width:400px;'
                }
            ),        
        }
    # help_texts = {
    #         'tags': '콤마로 구분하여 입력해주세요',
    #     }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].label = '태그'
        category_choices = kwargs.pop('category_choices', None)
        super(PostForm, self).__init__(*args, **kwargs)
        if category_choices:
            self.fields['category'].choices = category_choices

    class Meta:
        model = Post
        fields = ('title', 'content', 'category', 'address', 'tags')

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '제목을 입력해주세요',
                    'style': 'width:400px;'
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
                    'style': 'width:350px;'
                }
            ),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['title'].widget.attrs['style'] = 'width:100%; border: none;'
        self.fields["content"].required = False
        self.fields['content'].label = '내용'
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['style'] = 'width:100%; border: none;'
        self.fields['address'].label = '주소'
        self.fields['address'].widget.attrs['style'] = 'width:100%; border: none;'
        self.fields['tags'].label = '태그'
        self.fields['tags'].widget.attrs['class'] = 'form-control'
        self.fields['tags'].widget.attrs['placeholder'] = '콤마로 구분하여 입력해주세요'
        self.fields['tags'].widget.attrs['style'] = 'width:100%; border: none;'
        # self.fields['created_at'].label = '생성일'
        # self.fields['updated_at'].label = '수정일'
        self.fields['category'].label = '분류'
        self.fields['category'].widget.attrs['style'] = 'width:100%; border: none;'


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
                'class': 'form-control',
                'placeholder': '내용을 입력해주세요.',
            }
        )
    )
    class Meta:
        model = Comment
        fields = (
            "content",
        )


class PostReportForm(forms.ModelForm):

    title = forms.ChoiceField(
        choices=PostReport.TITLE_CHOICES,
        label='분류(필수)',
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )
    content = forms.CharField(
        label='허위 신고자에게는  불이익이 발생할 수 있습니다. 신고 내용을 신중하게 생각하셔서, 정확하고 상세하게 기입해 주십시오.',
        widget=forms.Textarea(
            attrs={
              'class': 'form-control',
            }
        )
    )
    class Meta:
        model = PostReport
        fields = ('title', 'content')

class CommentReportForm(forms.ModelForm):

    title = forms.ChoiceField(
        choices=CommentReport.TITLE_CHOICES,
        label='분류(필수)',
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )
    content = forms.CharField(
        label='허위 신고자에게는  불이익이 발생할 수 있습니다. 신고 내용을 신중하게 생각하셔서, 정확하고 상세하게 기입해 주십시오.',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
    class Meta:
        model = CommentReport
        fields = ('title', 'content')