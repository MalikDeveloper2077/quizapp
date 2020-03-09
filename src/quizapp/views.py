from time import time

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator

from .models import Quiz, Question, QuizManager
from .forms import QuizCreateForm, CommentCreateForm
from .for_slug import slugify as my_slugify


class QuizList(ListView):
    """List of quizzes + pagination"""
    model = Quiz
    template_name = 'quizapp/home.html'
    context_object_name = 'quizzes'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'list'
        context['current_url'] = self.request.build_absolute_uri()
        return context


class QuizDetail(View):
    """Detail of a quiz. Add 1 view to quiz.views"""

    def get(self, request, slug):
        quiz = get_object_or_404(Quiz, slug=slug)
        form = CommentCreateForm()
        quiz.views += 1
        quiz.save()
        ctx = {
            'quiz': quiz,
            'form': form
        }
        return render(request, 'quizapp/quiz_detail.html', ctx)


class QuizCreate(LoginRequiredMixin, CreateView):
    """Create a quiz"""
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
    """Update a quiz"""
    model = Quiz
    form_class = QuizCreateForm
    template_name_suffix = '_update'

    def test_func(self):
        """Available only for a quiz author"""
        return self.get_object().author == self.request.user


class QuestionList(ListView):
    """List of quiz questions and paginate it by 1 page"""
    model = Question
    template_name = 'quizapp/question_list.html'
    context_object_name = 'questions'
    paginate_by = 1

    def get_queryset(self):
        quiz = get_object_or_404(Quiz, slug=self.kwargs['slug'])
        queryset = super().get_queryset()
        queryset = queryset.filter(quiz=quiz)
        return queryset


class QuizComplete(View):
    """Complete a quiz.

    Get quiz via slug. Get QuizManager via quiz and request.user.
    QuizManager.completed set to True and save.
    Define result_state based on the number of correct answers.

    Args:
        slug(str): quiz slug

    Returns:
        correct_answers(int): number of correct answers from user in the quiz
        all_answers(int): number of all answers
        result_state(str): end state of the quiz passing

    """

    def get(self, request, slug):
        quiz = get_object_or_404(Quiz, slug=slug)
        quiz_manager = get_object_or_404(
            QuizManager, quiz=quiz, user=request.user)
        quiz_manager.completed = True
        quiz_manager.save()

        # TODO: increase user xp in the different if statements
        if quiz_manager.correct_answers == quiz.get_questions_count():
            result_state = 'awesome'

        elif quiz_manager.correct_answers > quiz.get_questions_count() / 1.5 and \
                quiz_manager.correct_answers < quiz.get_questions_count():
            result_state = 'good'

        elif quiz_manager.correct_answers > quiz.get_questions_count() / 2.5 and \
                quiz_manager.correct_answers < quiz.get_questions_count() / 1.5:
            result_state = 'normal'

        else:
            result_state = 'bad'

        ctx = {
            'correct_answers': quiz_manager.correct_answers,
            'all_answers': quiz.get_questions_count(),
            'result_state': result_state
        }

        return render(request, 'quizapp/quiz_complete.html', ctx)
