from django.db import models
from django.conf import settings


LEVEL_CHOICES = [
    ('easy', 'Легко'),
    ('normal', 'Средне'),
    ('hard', 'Сложно'),
    ('extreme', 'Очень сложно'),
]


class Quiz(models.Model):
    """Quiz model"""
    title = models.CharField('Название', max_length=80)
    body = models.TextField('Описание', blank=True)
    date = models.DateTimeField('Дата создания', auto_now_add=True)
    views = models.IntegerField('Просмотры', default=0)
    level = models.CharField('Уровень', max_length=20, choices=LEVEL_CHOICES)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Понравилось",
        related_name="liked_quizzes"
    )
    completed = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Пройдено",
        related_name="completed_quizzes",
    )
    photo = models.ImageField(
        'Картинка',
        upload_to='main_quiz_photos/%Y/%m/%d',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Викторина'
        verbose_name_plural = 'Викторины'
        ordering = ['-date']
