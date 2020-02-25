from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from quizapp.models import Quiz


class QuizDeleteAPI(APIView):
    """API for delete the quiz"""
    def get(self, request, slug):
        quiz = get_object_or_404(Quiz, slug=slug)
        quiz.delete()
        return Response(status=status.HTTP_200_OK)
