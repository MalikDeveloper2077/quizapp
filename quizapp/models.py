from time import time

from django.db import models
from django.conf import settings
from .for_slug import slugify as my_slugify


LEVEL_CHOICES = [
    ('Легко', 'easy'),
    ('Средне', 'normal'),
    ('Сложно', 'hard'),
    ('Очень сложно', 'extreme'),
]


class Quiz(models.Model):
    """Quiz model"""
    slug = models.SlugField('Url-адрес', max_length=50, blank=True)
    title = models.CharField('Название', max_length=50)
    body = models.TextField('Описание', blank=True)
    date = models.DateTimeField('Дата создания', auto_now_add=True)
    views = models.IntegerField('Просмотры', default=0)
    level = models.CharField('Уровень', max_length=20, choices=LEVEL_CHOICES)
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
        'Картинка',
        upload_to='main_quiz_photos/%Y/%m/%d',
        blank=True,
        null=True
    )

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
