from django.urls import path

from . import views


urlpatterns = [
    path('quiz/delete/<slug:slug>/', views.QuizDeleteAPI.as_view(), name="quiz-delete-api"),
    path('comment/create/<slug:slug>/', views.CommentCreateAPI.as_view(), name="comment-create"),
    path('comment/delete/<int:pk>/', views.CommentDeleteAPI.as_view(), name="comment-delete")
]
