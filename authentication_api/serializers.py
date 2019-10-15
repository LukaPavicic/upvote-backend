from rest_framework import serializers
from .models import User, Community, UserJoinedCommunity, Post, Comment, Upvote, Save
from rest_framework.fields import CurrentUserDefault

class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'upvotes', 'created_at', 'profile_image')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input': 'password'},                
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = User.objects.create_user(email=validated_data['email'], username=validated_data['username'], password=validated_data['password'])

        return user


class CommunitySerializer(serializers.ModelSerializer):
    """Community model serializer"""

    has_user_joined = serializers.SerializerMethodField('has_user_joined_field')

    def has_user_joined_field(self, obj):
        """Check if user joined current community"""
        if UserJoinedCommunity.objects.filter(user=self.context['request'].user, community=obj.id).exists():
            return 1
        else:
            return 0

    class Meta:
        model = Community
        fields = ('id', 'name', 'description', 'created_by', 'created_at', 'number_of_members', 'has_user_joined', 'community_image')
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
        }

    def create(self, validated_data):
        return UserJoinedCommunity.objects.create(**validated_data)
        

class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts"""  

    post_upvotes = serializers.SerializerMethodField('post_upvotes_field')
    has_user_upvoted = serializers.SerializerMethodField('has_user_upvoted_field')
    has_user_saved = serializers.SerializerMethodField('has_user_saved_field')

    def post_upvotes_field(self, obj):        
        return len(obj.upvote_set.all())

    def has_user_saved_field(self, obj):
        user = self.context['request'].user
        if Save.objects.filter(user=user, post=obj.id).exists():
            return 1
        else:
            return 0

    def has_user_upvoted_field(self, obj):
        user = self.context['request'].user
        if Upvote.objects.filter(user=user, post=obj.id).exists():
            return 1
        else:
            return 0
        

    class Meta:
        model = Post        
        fields = ('id', 'title', 'description', 'created_at', 'author', 'community', 'post_upvotes', 'has_user_upvoted', 'has_user_saved', 'post_image')
        extra_kwargs = {
            'author': {
                'read_only': True
            }
        }
        

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = UserSerializer(instance.author, context=self.context).data
        representation['community'] = CommunitySerializer(instance.community, context=self.context).data
        return representation


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments"""

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'created_at', 'post')
        extra_kwargs = {
            'author': {
                'read_only': True
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = UserSerializer(instance.author).data
        return representation


class UpvoteSerializer(serializers.ModelSerializer):
    """Serializer for upvotes"""

    class Meta:
        model = Upvote
        fields = ('id', 'user', 'post')
        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }


class SaveSerializer(serializers.ModelSerializer):
    """Serializer for user saved posts"""

    class Meta:
        model = Save
        fields = ('id', 'user', 'post')
        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['post'] = PostSerializer(instance.post, context=self.context).data
        return representation
        