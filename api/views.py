from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics

from quizapp.models import Quiz, Comment
from .serializers import CommentSerializer


class QuizDeleteAPI(generics.DestroyAPIView):
    """API for delete a quiz"""
    queryset = Quiz.objects.all()
    lookup_field = 'slug'


class CommentDeleteAPI(generics.DestroyAPIView):
    """API for delete a comment"""
    queryset = Comment.objects.all()


class CommentCreateAPI(APIView):
    """API for create a quiz comment. Get a quiz slug"""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, slug):
        quiz = get_object_or_404(Quiz, slug=slug)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, quiz=quiz)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
