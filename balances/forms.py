from django import forms
from .models import Question




class QuestionForm(forms.ModelForm):
    title = forms.CharField(
        max_length=1000,
        required=True,
        label='Q',
        widget=forms.TextInput(
            attrs={
                
                
            }
        )
    )
    content1 = forms.CharField(
        max_length=1000,
        label='A1',
        widget=forms.Textarea(
            attrs={
                
            }
        )
    )
    content2 = forms.CharField(
        max_length=1000,
        label='A2',
        widget=forms.Textarea(
            attrs={
                
            }
        )
    )

    image1 = forms.ImageField(
        label='A1_img',
        required=False,
        widget=forms.ClearableFileInput(
        attrs={
            }
        )
    )

    image2 = forms.ImageField(
        label='A2_img',
        required=False,
        widget=forms.ClearableFileInput(
        attrs={
            }
        )
    )


    class Meta:
        model = Question
        fields = ('title', 'content1','content2','image1','image2')




