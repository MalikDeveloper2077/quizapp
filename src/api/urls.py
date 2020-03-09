from django.urls import path

from . import views


urlpatterns = [
    path('quiz/<slug:slug>/delete/',
         views.QuizDeleteAPI.as_view(), name="quiz-delete-api"),
    path('quiz/like-unlike/', views.QuizLikeUnlikeAPI.as_view(),
         name="quiz-like-unlike-api"),
    path('quiz/<slug:slug>/comment/create/',
         views.CommentCreateAPI.as_view(), name="comment-create-api"),
    path('quiz/comment/delete/<int:pk>/',
         views.CommentDeleteAPI.as_view(), name="comment-delete-api"),
    path('quiz/bookmark/create-remove/', views.CreateRemoveBookmarkAPI.as_view(),
         name="bookmark-create-remove-api"),
    path('quiz/<slug:slug>/check-answer/',
         views.CheckAnswerAPI.as_view(), name="check-answer"),
]
