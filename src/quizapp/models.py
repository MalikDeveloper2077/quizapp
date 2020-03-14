from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.db.models import F

from .for_slug import slugify as my_slugify


LEVEL_CHOICES = [
    ('Легко', 'легко'),
    ('Средне', 'средне'),
    ('Сложно', 'сложно'),
    ('Экстремально', 'экстремально'),
]


class Quiz(models.Model):
    """Quiz model"""
    slug = models.SlugField(
        'Url-адрес',
        max_length=60,
        unique=True,
        db_index=True
    )
    title = models.CharField('Название', max_length=50)
    body = models.TextField('Описание', blank=True)
    date = models.DateTimeField('Дата создания', auto_now_add=True)
    views = models.IntegerField('Просмотры', default=0)
    level = models.CharField('Уровень', max_length=20, choices=LEVEL_CHOICES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quizzes',
        verbose_name='Автор',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='quiz',
        blank=True,
        null=True
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Понравилось",
        related_name="liked_quizzes",
        blank=True
    )
    photo = models.ImageField(
        'Фото',
        upload_to='main_quiz_photos/%Y/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Викторина'
        verbose_name_plural = 'Викторины'
        ordering = ['-date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Use the custom slugify (for_slug.py) and add
        generated slug + self.id in self.slug
        """
        slug = my_slugify(self.title)
        self.slug = slug + f'-{self.id}'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('quiz-detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('quiz-update', kwargs={'slug': self.slug})

    def get_question_list_url(self):
        return reverse('question-list', kwargs={'slug': self.slug})

    def get_manage_questions_url(self):
        return reverse('manage-questions', kwargs={'slug': self.slug})

    def get_likes_count(self):
        return self.likes.count()

    def get_completed_count(self):
        return QuizManager.objects.filter(quiz=self, completed=True).count()

    def get_comments_count(self):
        return self.comments.count()

    def get_bookmarks_count(self):
        return self.bookmarks.count()

    def get_questions_count(self):
        return self.questions.count()

    def get_bookmarks_users(self):
        """Get all users id who bookmarked the quiz"""
        users_id = []

        for bookmark in self.bookmarks.values('user'):
            users_id.append(bookmark['user'])

        return users_id

    def bookmark_quiz(self, quiz, user, bookmark):
        """Bookmark a quiz

        If bookmark is exists -> delete else create

        Args:
            quiz(obj): quiz to be (un)bookmarked
            user(obj): user who want to (un)bookmark the quiz
            bookmark(obj): queryset to find a bookmark

        Returns:
            data(dict):
                bookmarked(bool): quiz was bookmarked - True else False
                bookmarks(int): count of all bookmarks at the quiz

        """
        data = {}

        if bookmark.exists():
            bookmark.delete()
            data['bookmarked'] = False
        else:
            Bookmark.objects.create(quiz=quiz, user=user)
            data['bookmarked'] = True

        data['bookmarks'] = quiz.get_bookmarks_count()

        return data

    def like_quiz(self, quiz, user):
        """Like a quiz

        If user already liked the quiz -> remove it else add like

        Args:
            quiz(obj): quiz to be (un)liked
            user(obj): user who want to (un)like the quiz

        Returns:
            data(dict):
                liked(bool): quiz was liked - True else False
                likes(int): count of all likes at the quiz

        """
        data = {}

        if user in quiz.likes.all():
            quiz.likes.remove(user)
            data['liked'] = False
        else:
            quiz.likes.add(user)
            data['liked'] = True

        data['likes'] = quiz.get_likes_count()

        return data

    def increase_views(self):
        """Increase views field at the quiz"""
        self.views += 1
        self.save(update_fields=('views',))


class QuizManager(models.Model):
    """Manager for a quiz. Create when a user starts a quiz.

    Attributes:
        correct_answers(int): stores correct answers.
        completed(boolean): state of a quiz passing.

    """
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='managers',
        verbose_name='Викторина'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='managers',
        verbose_name='Пользователь'
    )
    date = models.DateTimeField(
        'Дата создания', auto_now_add=True, blank=True, null=True
    )
    correct_answers = models.PositiveSmallIntegerField(
        'Правильные ответы',
        default=0
    )
    completed = models.BooleanField('Завершено', default=False)

    class Meta:
        verbose_name = 'Менеджер викторины'
        verbose_name_plural = 'Менеджеры викторин'

    def __str__(self):
        return f'{self.quiz}-{self.user}'

    def get_correct_answers(self):
        return self.correct_answers

    def increase_correct_answers(self):
        """Increase the correct_answers field"""
        self.correct_answers = F('correct_answers') + 1
        self.save(update_fields=('correct_answers',))

    def remove_correct_answers(self):
        """Set correct answers field as 0"""
        self.correct_answers = 0
        self.save(update_fields=('correct_answers',))

    def set_as_completed(self):
        """Set the completed field to True"""
        self.completed = True
        self.save(update_fields=('completed',))

    def set_as_uncompleted(self):
        """Set the completed field to False"""
        self.completed = False
        self.save(update_fields=('completed',))

    def get_passing_status(self, quiz):
        """Return the quiz passing status.

        Calculate different between QuizManager.correct_answers count
        and quiz.questions couns. Set status as awesome, good, normal or bad

        Args:
            quiz(obj): quiz for checking

        Returns:
            status(str): result status of the passing

        """
        # TODO: increase user xp in the different if statements
        if self.correct_answers == quiz.get_questions_count():
            status = 'Потрясающе 😍'

        elif self.correct_answers > quiz.get_questions_count() / 1.5 and \
                self.correct_answers < quiz.get_questions_count():
            status = 'Отлично 👍'

        elif self.correct_answers > quiz.get_questions_count() / 2.5 and \
                self.correct_answers < quiz.get_questions_count() / 1.5:
            status = 'Неплохо 😁'

        else:
            status = 'Не огорчайся 😕'

        return status


class Category(models.Model):
    """Category for quizzes"""
    name = models.CharField('Имя категории', max_length=30)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Comment(models.Model):
    """Comment for a quiz"""
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name='Викторина',
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='Автор',
        related_name='comments'
    )
    body = models.TextField('Текст')
    date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-date']

    def __str__(self):
        return self.body


class Bookmark(models.Model):
    """Bookmar for a quiz"""
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name='Викторина',
        related_name='bookmarks'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='bookmarks'
    )
    date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'
        ordering = ['-date']

    def __str__(self):
        return f'{self.user} - {self.quiz}'


class Question(models.Model):
    """Question for a quiz. Has foreign key to a Quiz"""
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name='Викторина',
        related_name='questions'
    )
    title = models.CharField('Вопрос', max_length=100)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.title


class QuestionAnswer(models.Model):
    """Answer to the question. Has foreign key to a Question"""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
        related_name='answers'
    )
    value = models.CharField('Ответ', max_length=50)
    is_correct = models.BooleanField('Корректность', default=False)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.value
