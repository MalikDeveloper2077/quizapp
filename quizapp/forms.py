from django import forms
from django.core.exceptions import ValidationError

from .models import Quiz


class QuizCreateForm(forms.ModelForm):
    """Form for create a quiz"""
    class Meta:
        model = Quiz
        fields = ['title', 'body', 'level', 'category', 'photo']
