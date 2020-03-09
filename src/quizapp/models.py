from django.db import models
from django.conf import settings
from django.urls import reverse

from .for_slug import slugify as my_slugify


LEVEL_CHOICES = [
    ('Легко', 'легко'),
    ('Средне', 'средне'),
    ('Сложно', 'сложно'),
    ('Экстремально', 'экстремально'),
]


class Quiz(models.Model):
    """Quiz model"""
    slug = models.SlugField('Url-адрес', max_length=60)
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

    def get_absolute_url(self):
        return reverse('quiz-detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('quiz-update', kwargs={'slug': self.slug})

    def get_question_list_url(self):
        return reverse('question-list', kwargs={'slug': self.slug})

    def get_likes_count(self):
        return self.likes.count()

    def get_completed_count(self):
        return QuizManager.objects.filter(quiz=self, completed=True).count()

    def get_comments_count(self):
        return self.comments.count()

    def get_bookmarks_count(self):
        return self.bookmarks.count()

    def get_bookmarks_users(self):
        """Get all users who bookmarked the quiz"""
        bookmark_users = []

        for bookmark in self.bookmarks.all():
            bookmark_users.append(bookmark.user)

        return bookmark_users

    def get_questions_count(self):
        return self.questions.count()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Use the custom slugify (for_slug.py) and add
        generated slug + self.id in self.slug
        """
        slug = my_slugify(self.title)
        self.slug = slug + f'-{self.id}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Викторина'
        verbose_name_plural = 'Викторины'
        ordering = ['-date']


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
    correct_answers = models.IntegerField('Правильные ответы', default=0)
    completed = models.BooleanField('Завершено', default=False)

    def __str__(self):
        return f'{self.quiz}-{self.user}'

    class Meta:
        verbose_name = 'Менеджер викторины'
        verbose_name_plural = 'Менеджеры викторин'


class Category(models.Model):
    """Category for quizzes"""
    name = models.CharField('Имя категории', max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


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

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-date']


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

    def __str__(self):
        return f'{self.user} - {self.quiz}'

    class Meta:
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'
        ordering = ['-date']


class Question(models.Model):
    """Question for a quiz. Has foreign key to a Quiz"""
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name='Викторина',
        related_name='questions'
    )
    title = models.CharField('Вопрос', max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


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

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
