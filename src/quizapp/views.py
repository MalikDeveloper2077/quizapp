from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count

from .models import Quiz, Question, QuizManager
from .forms import QuizCreateForm, CommentCreateForm
from .filters import QuizFilter


class QuizList(ListView):
    """List of quizzes"""
    model = Quiz
    template_name = 'quizapp/home.html'
    context_object_name = 'quizzes'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        """Additional context.

        active: for know which page was opened
        current_url: absolute_url at a current page
        filter: form for filtering quizzes

        """
        context = super().get_context_data(**kwargs)
        context['active'] = 'list'
        context['current_url'] = self.request.build_absolute_uri()
        context['filter_form'] = QuizFilter(
            self.request.GET, queryset=self.model.objects.all()
        ).form
        return context

    def get_queryset(self):
        qs = self.model.objects.all()
        filtered_quizzes = QuizFilter(self.request.GET, queryset=qs)
        return filtered_quizzes.qs


class QuizListMostViewed(ListView):
    """List of most viewed quizzes"""
    model = Quiz
    template_name = 'quizapp/home.html'
    context_object_name = 'quizzes'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'most_viewed'
        context['current_url'] = self.request.build_absolute_uri()
        context['filter_form'] = QuizFilter(
            self.request.GET, queryset=self.model.objects.all()
        ).form
        return context

    def get_queryset(self):
        qs = self.model.objects.order_by('-views')
        filtered_quizzes = QuizFilter(self.request.GET, queryset=qs)
        return filtered_quizzes.qs


class QuizListMostLiked(ListView):
    """List of most viewed quizzes"""
    model = Quiz
    template_name = 'quizapp/home.html'
    context_object_name = 'quizzes'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'most_liked'
        context['current_url'] = self.request.build_absolute_uri()
        context['filter_form'] = QuizFilter(
            self.request.GET, queryset=self.model.objects.all()
        ).form
        return context

    def get_queryset(self):
        qs = self.model.objects.all().annotate(cnt=Count('likes')).order_by('-cnt')
        filtered_quizzes = QuizFilter(self.request.GET, queryset=qs)
        return filtered_quizzes.qs


class QuizUserList(ListView):
    """List of most viewed quizzes"""
    model = Quiz
    template_name = 'quizapp/home.html'
    context_object_name = 'quizzes'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'my_quizzes'
        context['current_url'] = self.request.build_absolute_uri()
        context['filter_form'] = QuizFilter(
            self.request.GET, queryset=self.model.objects.all()
        ).form
        return context

    def get_queryset(self):
        qs = self.request.user.quizzes.all()
        filtered_quizzes = QuizFilter(self.request.GET, queryset=qs)
        return filtered_quizzes.qs


class QuizDetail(View):
    """Detail of a quiz. Call Quiz.increase_views() method"""

    def get(self, request, slug):
        quiz = get_object_or_404(Quiz, slug=slug)
        form = CommentCreateForm()

        quiz.increase_views()

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
    """List of quiz questions

    Template name and count for pagination get in url args

    Url args:
        slug(str): slug of a quiz which contains questions

    """
    model = Question
    context_object_name = 'questions'

    def get_queryset(self):
        quiz = get_object_or_404(Quiz, slug=self.kwargs['slug'])
        queryset = super().get_queryset()
        queryset = queryset.filter(quiz=quiz)
        return queryset


class QuizComplete(View):
    """Complete a quiz.

    Get quiz via slug. Get QuizManager via quiz and request.user.
    Call QuizManager and Profile methods to complete the quiz,
    get result status, and increase_xp.
    If profile level need to upgrade call Profile.get_next_level
    and Profile.level_up()

    Args:
        slug(str): quiz slug

    Returns:
        correct_answers(int): number of correct answers from user in the quiz
        all_answers(int): number of all answers
        passing_status(str): end status of the quiz passing
        increased_xp(int): xp that was increased
        level_up(bool): if profile.level_up was called True else False

    """

    def get(self, request, slug):
        quiz = get_object_or_404(Quiz, slug=slug)
        quiz_manager = get_object_or_404(
            QuizManager,
            quiz=quiz,
            user=request.user
        )

        # Complete and increase xp
        quiz_manager.set_as_completed()
        passing_status = quiz_manager.get_passing_status(quiz)
        required_xp = quiz_manager.calculate_required_xp_count(passing_status)
        request.user.profile.increase_xp(required_xp)

        # Level up if necessary
        level_up = False

        if request.user.profile.check_level_up():
            next_level = request.user.profile.get_next_level()
            request.user.profile.level_up(next_level)
            level_up = True

        ctx = {
            'correct_answers': quiz_manager.get_correct_answers(),
            'all_answers': quiz.get_questions_count(),
            'passing_status': passing_status,
            'increased_xp': required_xp,
            'level_up': level_up
        }

        return render(request, 'quizapp/quiz_complete.html', ctx)
