from django import forms
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class ComposeMessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['receiver'].queryset = User.objects.exclude(id=user.id)

    class Meta:
        model = Message
        fields = ['receiver', 'content']
    class Meta:
        model = Message
        fields = ['receiver', 'content']
        widgets = {
            'receiver': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
