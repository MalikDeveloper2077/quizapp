from django.urls import path

from . import views


urlpatterns = [
    path('', views.QuizList.as_view(), name="home")
]
