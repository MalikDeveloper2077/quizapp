from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from quizapp.models import Quiz, Comment, Bookmark
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
    Create or remove bookmark at that quiz

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
