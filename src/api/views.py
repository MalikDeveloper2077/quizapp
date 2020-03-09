from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from quizapp.models import Quiz, Comment, Bookmark, QuestionAnswer, QuizManager
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
        liked(bool): if user liked the quiz True otherwise False
        likes(int): count of quiz likes
        response status 200

    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        quiz = get_object_or_404(Quiz, slug=request.GET['slug'])
        data = {}

        if request.user in quiz.likes.all():
            quiz.likes.remove(request.user)
            data['liked'] = False
        else:
            quiz.likes.add(request.user)
            data['liked'] = True

        data['likes'] = quiz.get_likes_count()

        return Response(data, status=status.HTTP_200_OK)


class CreateRemoveBookmarkAPI(APIView):
    """API for creating or removing quiz bookmark.

    Get a quiz slug from request.data.
    Create or delete bookmark at that quiz.

    Request data args:
        slug(str): slug of the quiz

    Returns:
        bookmarked(bool): if user bookmarked the quiz True otherwise False
        bookmarks(int): count of quiz bookmarks
        response status 200

    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        quiz = get_object_or_404(Quiz, slug=request.data['slug'])
        bookmark = Bookmark.objects.filter(quiz=quiz, user=request.user)
        data = {}

        if bookmark.exists():
            bookmark.delete()
            data['bookmarked'] = False
        else:
            Bookmark.objects.create(quiz=quiz, user=request.user)
            data['bookmarked'] = True

        data['bookmarks'] = quiz.get_bookmarks_count()

        return Response(data, status=status.HTTP_200_OK)


class CheckAnswerAPI(APIView):
    """API for checking answers. 

    Find the quiz with given slug.
    Get a pk from the GET data and find the answer.

    If a user already completed the quiz set correct_answers = 0
    and completed = False, save it. User will pass the quiz from scratchю

    Check if the answer is correct -> increase the quiz manager 
    correct_answers by 1 and save it.

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

        if quiz_manager.completed:
            quiz_manager.correct_answers = 0
            quiz_manager.completed = False
            quiz_manager.save()

        if answer.is_correct:
            quiz_manager.correct_answers += 1
            quiz_manager.save()

        return Response({'checked': True}, status=status.HTTP_200_OK)
