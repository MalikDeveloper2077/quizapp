from time import time

from django.db import models
from django.conf import settings
from django.urls import reverse

from .for_slug import slugify as my_slugify


LEVEL_CHOICES = [
    ('Легко', 'easy'),
    ('Средне', 'normal'),
    ('Сложно', 'hard'),
    ('Экстремально', 'extreme'),
]


class Quiz(models.Model):
    """Quiz model"""
    slug = models.SlugField('Url-адрес', max_length=50, blank=True)
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
    completed = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Пройдено",
        related_name="completed_quizzes",
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

    def get_likes_count(self):
        return self.likes.count()

    def get_completed_count(self):
        return self.completed.count()

    def get_comments_count(self):
        return self.comments.count()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Use the custom slugfiy (for_slug.py)"""
        if not self.slug:
            slug = my_slugify(self.title)
            exists = Quiz.objects.filter(slug=slug).exists()

            if exists:
                slug += f'-{str(int(time()))}'

            self.slug = slug
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Викторина'
        verbose_name_plural = 'Викторины'
        ordering = ['-date']


class Category(models.Model):
    """Category for the quiz"""
    name = models.CharField('Имя категории', max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Comment(models.Model):
    """Comment for the quiz"""
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
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-date']


class Question(models.Model):
    """Question for the quiz. Has foreign key to the Quiz"""
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name='Викторина',
        related_name='questions'
    )
    title = models.CharField('Вопрос', max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class QuestionAnswer(models.Model):
    """Answer to the question. Has foreign key to the Question"""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
        related_name='answers'
    )
    value = models.CharField('Ответ', max_length=150)
    is_correct = models.BooleanField('Корректность', default=False)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
