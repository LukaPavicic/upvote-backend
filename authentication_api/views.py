from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Community, UserJoinedCommunity, Post, Comment, Upvote, Save
from . import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from . import permissions
from rest_framework.settings import api_settings
from django.db.models import Case, When
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.parsers import FileUploadParser


class UserViewSet(viewsets.ModelViewSet):
    """Viewset for User model"""
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    def retrieve(self, request, *args, **kwargs):
        """Get all necessary user data"""
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = serializers.UserSerializer(user)
        user_posts = serializers.PostSerializer(Post.objects.all(), many=True, context={'request': request})
        final_user_posts = []
        for i in range(0, len(user_posts.data)):
            if(user_posts.data[i]["author"]["id"] == user.id):
                final_user_posts.append(user_posts.data[i])

        return Response({'user_info': serializer.data, 'user_posts': final_user_posts}, status=status.HTTP_200_OK)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CurrentUserApiView(APIView):
    """Get current user data"""
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        return Response({'user_id': request.user.id}, status=status.HTTP_200_OK)


class UserRelevantPosts(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user_relevant_posts = "?"
        return Response({'posts': user_relevant_posts}, status=status.HTTP_200_OK)


class CommunityViewSet(viewsets.ModelViewSet):
    """Handle CRUD for Communities"""
    serializer_class = serializers.CommunitySerializer
    queryset = Community.objects.all()
    authentication_classes = (TokenAuthentication,)
    parser_class = (FileUploadParser,)

    def retrieve(self, request, *args, **kwargs):
        """Get community data"""
        try:
            community = Community.objects.get(pk=kwargs['pk'])
        except Community.DoesNotExist:
            return Response({'error_message': 'Community not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommunitySerializer(community, context={'request': request})
        community_posts = serializers.PostSerializer(community.post_set.all(), many=True, context={'request': request})

        return Response({'community_data': serializer.data, 'community_posts': community_posts.data}, status=status.HTTP_200_OK)


    def perform_create(self, serializer):
        """Set created_by to current user"""
        serializer.save(created_by=self.request.user)  


class UpvoteViewSet(viewsets.ModelViewSet):
    """ViewSet for Upvote model"""
    queryset = Upvote.objects.all()   
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.UpvoteSerializer   

    def create(self, request, *args, **kwargs):
        if Upvote.objects.filter(user=request.user.id, post=request.data['post']).exists():
            Upvote.objects.filter(user=request.user.id, post=request.data['post']).first().delete()
            return Response({'message': 'Upvote removed'}, status=status.HTTP_200_OK)
        else:
            return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    """Handle CRUD for Posts"""
    serializer_class = serializers.PostSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = Post.objects.all()
    permission_classes = (permissions.DeleteOwnPost,)

    def retrieve(self, request, *args, **kwargs):        
        """Get all posts"""
        # post = get_object_or_404(self.queryset, pk=kwargs['pk'])
        try:
            post = Post.objects.get(pk=kwargs['pk'])
        except Post.DoesNotExist:
            return Response({'error_message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.PostSerializer(post, context={'request': request})
        post_comments = serializers.CommentSerializer(post.comment_set.all(), many=True)

        return Response({'post_data': serializer.data, 'post_comments': post_comments.data}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """Set author to current user"""
        serializer.save(author=self.request.user)  


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = Comment.objects.all() 
    permission_classes = (permissions.DeleteOwnComment,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  


class SaveViewSet(viewsets.ModelViewSet):
    """ViewSet for user saved posts"""
    authentication_classes = (TokenAuthentication,)
    queryset = Save.objects.all()
    serializer_class = serializers.SaveSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if Save.objects.filter(user=request.user, post=request.data['post']).exists():
            Save.objects.filter(user=request.user, post=request.data['post']).delete()
            return Response({'message': 'Save removed'}, status=status.HTTP_200_OK)
        else:
            return super().create(request, *args, **kwargs)

    def list(self, request):
        user = User.objects.get(pk=request.user.id)
        user_saved_posts = serializers.SaveSerializer(user.save_set.all(), many=True, context={'request': request})
        return Response({'saved_posts': user_saved_posts.data}, status=status.HTTP_200_OK)


class UserJoinedCommunityViewSet(viewsets.ModelViewSet):
    """Handle CRUD for User joined communities"""

    serializer_class = serializers.UserJoinedCommunitySerializer
    queryset = UserJoinedCommunity.objects.all()
    authentication_classes = (TokenAuthentication,)

    def list(self, request):
        
        com_pk_list = []

        joined_communites_ids = list(UserJoinedCommunity.objects.all().filter(user=request.user).values('community')[:5])

        for i in range(0,len(joined_communites_ids)):
            com_pk_list.append(joined_communites_ids[i]['community'])

        # preserved = Case(*[When(pk=pk, tehn=pos) for pos, pk in enumerate(com_pk_list)])
        queryset = Community.objects.filter(pk__in=com_pk_list).values('id', 'name')


        context = {
            'joined_communities': list(queryset)
        }        

        return Response(context)

    def create(self, request, *args, **kwargs):
        try:            
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            UserJoinedCommunity.objects.filter(user=request.user.id, community=request.data['community']).first().delete()
            return Response({'message': 'Left the community'}, status=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):
    #     if UserJoinedCommunity.objects.filter(user=request.user.id, community=request.data['community']).exists():
    #         UserJoinedCommunity.objects.filter(user=request.user.id, community=request.data['community']).first().delete()
    #         return Response({'message': 'Left the community'}, status=200)
    #     else:
    #         return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Add user to userjoinedcommunities"""
        serializer.save(user=self.request.user)
        

class UserRelevantPosts(APIView):
    """Get posts based on user joined communities"""
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        """Get method"""
        user = request.user
        joined_communities = []
        posts = []

        for item in UserJoinedCommunity.objects.filter(user=user).all():
            joined_communities.append(item.community.id)

        for post in Post.objects.all():
            if post.community.id in joined_communities:                
                posts.append(post)

        return Response({'posts': serializers.PostSerializer(posts, many=True, context={'request': request}).data}, status=status.HTTP_200_OK)

        

