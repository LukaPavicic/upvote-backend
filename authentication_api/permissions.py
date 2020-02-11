from rest_framework import permissions
from authentication_api.models import Comment, Post, Community

class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit only their own profiles and not others"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id==request.user.id


class DeleteOwnComment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        comment = Comment.objects.filter(pk=obj.id).first()
        if request.user == comment.author:
            return Comment.objects.filter(pk=obj.id).delete()


class DeleteOwnPost(permissions.BasePermission):
    """Allow user to delete only their own posts"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        post = Post.objects.filter(pk=obj.id).first()

        if request.user == post.author:
            return Post.objects.filter(pk=obj.id).delete()


class DeleteOwnCommunity(permissions.BasePermission):
    """Allow user to delete only their own communities"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        community = Community.objects.filter(pk=obj.id).first()

        if request.user == community.created_by:
            return community.delete

