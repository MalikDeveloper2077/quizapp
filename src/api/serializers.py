from rest_framework import serializers

from quizapp.models import Comment, Bookmark


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']
