from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from quizapp.models import (Quiz, Comment, Bookmark, QuestionAnswer,
                            QuizManager)
from .serializers import CommentSerializer
from .permissions import IsQuizOrCommentAuthor


class QuizDeleteAPI(generics.DestroyAPIView):
    """API for deleting a quiz"""
    queryset = Quiz.objects.all()
    lookup_field = 'slug'
    permission_classes = (IsAuthenticated, IsQuizOrCommentAuthor,)


class CommentDeleteAPI(generics.DestroyAPIView):
    """API for deleting a comment"""
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated, IsQuizOrCommentAuthor,)


class CommentCreateAPI(generics.CreateAPIView):
    """API for creating a quiz comment.

    Get a quiz slug kwarg. Find the quiz via slug and
    Save serializer with author=request.user and quiz=quiz

    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        quiz = get_object_or_404(Quiz, slug=self.kwargs['slug'])
        serializer.save(author=self.request.user, quiz=quiz)


class QuizLikeUnlikeAPI(APIView):
    """API for like and unlike a quiz.

    Add or remove user to quiz.likes relationship.
    Use quiz slug from request.GET data

    Request data args:
        slug(str): quiz slug for finding the quiz

    Returns:
        data(dict): contains returned data from quiz.like_quiz() method
        response status 200

    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        quiz = get_object_or_404(Quiz, slug=request.GET['slug'])
        data = quiz.like_quiz(quiz, request.user)

        return Response(data, status=status.HTTP_200_OK)


class CreateRemoveBookmarkAPI(APIView):
    """API for creating or removing quiz bookmark.

    Get a quiz slug from request.data.
    Create or delete bookmark at that quiz.

    Request data args:
        slug(str): slug of the quiz

    Returns:
        data(dict): contains returned data from quiz.bookmark_quiz() method
        response status 200

    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        quiz = get_object_or_404(Quiz, slug=request.data['slug'])
        bookmark = Bookmark.objects.filter(quiz=quiz, user=request.user)

        data = quiz.bookmark_quiz(quiz, request.user, bookmark)

        return Response(data, status=status.HTTP_200_OK)


class CheckAnswerAPI(APIView):
    """API for checking answers.

    Find the quiz with given slug.
    Get a pk from the GET data and find the answer.

    If a user already completed the quiz call QuizManager.set_as_uncompleted()
    and remove_correct_answers().
    User will pass the quiz from scratch.

    Check if the answer is correct -> increase the quiz manager
    correct_answers by QuizManager.increase_correct_answers().

    Args:
        slug(str): slug of the quiz question

    Request data args:
        pk(int): selected QuizAnswer pk

    Returns:
        checked(bool): True
        response status 200

    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, slug):
        quiz = get_object_or_404(Quiz, slug=slug)
        answer = get_object_or_404(QuestionAnswer, pk=request.GET.get('pk'))
        quiz_manager, created = QuizManager.objects.get_or_create(
            quiz=quiz,
            user=request.user
        )

        # Reset parameters if quiz is completed
        if quiz_manager.completed:
            quiz_manager.set_as_uncompleted()
            quiz_manager.remove_correct_answers()

        # Increase correct answers if answer is correct
        if answer.is_correct:
            quiz_manager.increase_correct_answers()

        return Response({'checked': True}, status=status.HTTP_200_OK)