from django import forms

from blog import models


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['body',]
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Write your comment here ...',
            })
        }

