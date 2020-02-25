from time import time

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError

from .models import Quiz
from .forms import QuizCreateForm
from .for_slug import slugify as my_slugify


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


class QuizDetail(View):
    """Detail of the quizzes. Added 1 view to quiz.views"""
    def get(self, request, slug):
        quiz = get_object_or_404(Quiz, slug=slug)
        quiz.views += 1
        quiz.save()
        return render(request, 'quizapp/quiz_detail.html', {'quiz': quiz})


class QuizCreate(LoginRequiredMixin, CreateView):
    """Create the quiz"""
    model = Quiz
    form_class = QuizCreateForm
    template_name_suffix = '_create'

    def form_valid(self, form):
        """Set author as the current user"""
        f = form.save(commit=False)
        f.author = self.request.user
        f.save()
        return super().form_valid(form)


class QuizUpdate(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    """Update the quiz"""
    model = Quiz
    form_class = QuizCreateForm
    template_name_suffix = '_update'

    def test_func(self):
        return self.get_object().author == self.request.user
