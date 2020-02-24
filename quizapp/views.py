from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Quiz
from .forms import QuizCreateForm


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


class QuizCreate(LoginRequiredMixin, CreateView):
    """Create the quiz"""
    model = Quiz
    form_class = QuizCreateForm
    template_name_suffix = '_create'
    success_url = reverse_lazy('home')  # TODO: success_url to the new quiz

    def form_valid(self, form):
        """Set author as the current user"""
        f = form.save(commit=False)
        f.author = self.request.user
        f.save()
        return super().form_valid(form)
