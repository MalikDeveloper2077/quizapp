from django.urls import path

from . import views


urlpatterns = [
    path('', views.QuizList.as_view(), name="home"),
    path('quiz/<slug:slug>/', views.QuizDetail.as_view(), name="quiz-detail"),
]
