from django.urls import path

from . import views


urlpatterns = [
    path('quiz/delete/<slug:slug>/', views.QuizDeleteAPI.as_view(), name="quiz-delete-api")
]
