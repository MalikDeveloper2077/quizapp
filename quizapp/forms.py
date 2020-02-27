from django import forms
from django.core.exceptions import ValidationError

from .models import Quiz, Comment


class QuizCreateForm(forms.ModelForm):
    """Form for create a quiz"""
    class Meta:
        model = Quiz
        fields = ['title', 'body', 'level', 'category', 'photo']


class CommentCreateForm(forms.ModelForm):
    """Form for create a quiz comment"""
    class Meta:
        model = Comment
        fields = ['body']

        widgets = {
            'body': forms.Textarea(attrs={'cols': 100, 'rows': 1,
                                'class': 'comment_create_body'})
        }

        labels = {
            'body': 'Комментарий'
        }
