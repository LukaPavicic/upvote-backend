from rest_framework import serializers
from .models import User, Community, UserJoinedCommunity, Post

class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'upvotes', 'created_at')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = User.objects.create_user(email=validated_data['email'], username=validated_data['username'], password=validated_data['password'])

        return user


class CommunitySerializer(serializers.ModelSerializer):
    """Community model serializer"""

    class Meta:
        model = Community
        fields = ('id', 'name', 'description', 'created_by', 'created_at', 'number_of_members')
        extra_kwargs = {
            'created_by': {
                'read_only': True
            }
        }


class UserJoinedCommunitySerializer(serializers.ModelSerializer):
    """Serializer for user joined communities"""

    class Meta:
        model = UserJoinedCommunity
        fields = ('id', 'user', 'community')
        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'community': {
                'read_only': True
            }
        }


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts"""
    # author = UserSerializer()
    # community = CommunitySerializer()

    class Meta:
        model = Post        
        fields = ('id', 'title', 'description', 'created_at', 'author', 'community')
        extra_kwargs = {
            'author': {
                'read_only': True
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = UserSerializer(instance.author).data
        representation['community'] = CommunitySerializer(instance.community).data
        return representation