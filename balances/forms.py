from django import forms
from .models import Question




class QuestionForm(forms.ModelForm):
    title = forms.CharField(
        max_length=1000,
        required=True,
        label='Q',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                
                
            }
        )
    )
    content1 = forms.CharField(
        max_length=1000,
        label='A1',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                
            }
        )
    )
    content2 = forms.CharField(
        max_length=1000,
        label='A2',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                
            }
        )
    )
    word1 = forms.CharField(
        max_length=100,
        required = False,
        label='word1',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                
            }
        )
    )

    word2 = forms.CharField(
        max_length=100,
        required = False,
        label='word2',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                
            }
        )
    )

    image1 = forms.ImageField(
        label='A1_img',
        required=False,
        widget=forms.ClearableFileInput(
        attrs={
                'class': 'form-control',
            }
        )
    )

    image2 = forms.ImageField(
        label='A2_img',
        required=False,
        widget=forms.ClearableFileInput(
        attrs={
                'class': 'form-control',
            }
        )
    )


    class Meta:
        model = Question
        fields = ('title', 'content1','content2','image1','image2', 'word1', 'word2')




