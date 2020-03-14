from django.urls import path

from . import views


urlpatterns = [
     # Quiz lists
     path('', views.QuizList.as_view(), name="home"),
     path('most-viewed/', views.QuizListMostViewed.as_view(),
          name="most-viewed"),
     path('most-liked/', views.QuizListMostLiked.as_view(), name="most-liked"),
     path('user-quizzes/', views.QuizUserList.as_view(), name="user-quizzes"),

     # Quiz detail
     path('quiz/<slug:slug>/', views.QuizDetail.as_view(), name="quiz-detail"),

     # Quiz passing
     path(
          'quiz/<slug:slug>/passing/',
          views.QuestionList.as_view(
               template_name='quizapp/question_list.html',
               paginate_by=1
          ),
          name="question-list"
     ),
     path(
          'quiz/<slug:slug>/complete/',
          views.QuizComplete.as_view(),
          name="quiz-complete"
     ),

     # Manage questions
     path(
          'quiz/<slug:slug>/manage-questions/',
          views.QuestionList.as_view(
               template_name='quizapp/questions_manage.html',
               paginate_by=15
          ),
          name="manage-questions"
     ),

     # Create and delete a quiz
     path('create/quiz/', views.QuizCreate.as_view(), name="quiz-create"),
     path(
          'update/quiz/<slug:slug>/',
          views.QuizUpdate.as_view(),
          name="quiz-update"
     ),
]
