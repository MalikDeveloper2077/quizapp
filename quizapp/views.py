from django.shortcuts import render
from django.views.generic import ListView

from .models import Quiz


class QuizList(ListView):
    model = Quiz
    template_name = 'quizapp/home.html'
    context_object_name = 'quizzes'
