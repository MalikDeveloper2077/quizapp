from rest_framework import permissions


class IsQuizOrCommentAuthor(permissions.BasePermission):
    """For deleting a quiz or a comment.

    If obj is a quiz -> available only to quiz authors
    If obj is a comment -> available only to comment authors

    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return request.user == obj.author
