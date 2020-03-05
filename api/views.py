from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from quizapp.models import Quiz, Comment, Bookmark
from .serializers import CommentSerializer
from .permissions import IsQuizOrCommentAuthor


class QuizDeleteAPI(generics.DestroyAPIView):
    """API for delete a quiz"""
    queryset = Quiz.objects.all()
    lookup_field = 'slug'
    permission_classes = (IsAuthenticated, IsQuizOrCommentAuthor,)


class CommentDeleteAPI(generics.DestroyAPIView):
    """API for delete a comment"""
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated, IsQuizOrCommentAuthor,)


class CommentCreateAPI(APIView):
    """API for create a quiz comment. Get a quiz slug"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, slug):
        quiz = get_object_or_404(Quiz, slug=slug)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, quiz=quiz)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizLikeUnlikeAPI(APIView):
    """API for like and unlike a quiz.
    Add or remove user to quiz.likes relationship
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
    """API for create or remove quiz bookmark.
    Get a quiz slug, and create or remove bookmark at it
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
