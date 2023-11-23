from django import forms

from blog.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'Share your thoughts in the comments...',
                'rows': 4
            })
        }

        labels = {
            'body': 'Add your comment'
        }

