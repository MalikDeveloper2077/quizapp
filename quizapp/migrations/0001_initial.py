# Generated by Django 3.0.3 on 2020-02-19 21:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Название')),
                ('body', models.TextField(blank=True, verbose_name='Описание')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('views', models.IntegerField(default=0, verbose_name='Просмотры')),
                ('level', models.CharField(choices=[('easy', 'Легко'), ('normal', 'Средне'), ('hard', 'Сложно'), ('extreme', 'Очень сложно')], max_length=20, verbose_name='Уровень')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='main_quiz_photos/%Y/%m/%d', verbose_name='Картинка')),
                ('completed', models.ManyToManyField(related_name='completed_quizzes', to=settings.AUTH_USER_MODEL, verbose_name='Понравилось')),
                ('likes', models.ManyToManyField(related_name='liked_quizzes', to=settings.AUTH_USER_MODEL, verbose_name='Понравилось')),
            ],
            options={
                'verbose_name': 'Викторина',
                'verbose_name_plural': 'Викторины',
                'ordering': ['-date'],
            },
        ),
    ]
