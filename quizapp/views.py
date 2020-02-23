from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Quiz


class QuizList(ListView):
    """List of the quizzes + paginate"""
    model = Quiz
    template_name = 'quizapp/home.html'
    context_object_name = 'quizzes'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'list'
        return context


class QuizDetail(DetailView):
    """Detail of the quizzes"""
    model = Quiz
    template_name = 'quizapp/quiz_detail.html'
    context_object_name = 'quiz'
