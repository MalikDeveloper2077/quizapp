from django.urls import path

from . import views


urlpatterns = [
    path('', views.QuizList.as_view(), name="home"),
    path('quiz/<slug:slug>/', views.QuizDetail.as_view(), name="quiz-detail"),
    path('quiz/<slug:slug>/passing/',
         views.QuestionList.as_view(), name="question-list"),
    path('quiz/<slug:slug>/complete/', views.QuizComplete.as_view(),
         name="quiz-complete"),
    path('create/quiz/', views.QuizCreate.as_view(), name="quiz-create"),
    path('update/quiz/<slug:slug>/',
         views.QuizUpdate.as_view(), name="quiz-update"),
]
