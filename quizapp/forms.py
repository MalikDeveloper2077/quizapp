from django import forms

from .models import Quiz


class QuizCreateForm(forms.ModelForm):
    """Form for create a quiz"""
    class Meta:
        model = Quiz
        fields = ['title', 'body', 'level', 'category', 'photo']
