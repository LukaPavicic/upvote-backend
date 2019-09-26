from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Community, UserJoinedCommunity, Post
from . import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from . import permissions
from rest_framework.settings import api_settings
from django.db.models import Case, When
from django.shortcuts import get_object_or_404


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
        user_posts = serializers.PostSerializer(Post.objects.all(), many=True)
        final_user_posts = []
        for i in range(0, len(user_posts.data)):
            if(user_posts.data[i]["author"]["id"] == user.id):
                final_user_posts.append(user_posts.data[i])

        return Response({'user_info': serializer.data, 'user_posts': final_user_posts})


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CurrentUserApiView(APIView):
    """Get current user data"""
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        return Response({'user_id': request.user.id})


# class UserCreatedPosts(APIView):
#     """Get user created posts"""
#     authentication_classes = (TokenAuthentication,)

#     def get(self, request):
#         """"""



class CommunityViewSet(viewsets.ModelViewSet):
    """Handle CRUD for Communities"""
    serializer_class = serializers.CommunitySerializer
    queryset = Community.objects.all()
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        """Set created_by to current user"""
        serializer.save(created_by=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    """Handle CRUD for Posts"""
    serializer_class = serializers.PostSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        """Set author to current user"""
        serializer.save(author=self.request.user)


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
        

