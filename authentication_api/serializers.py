from rest_framework import serializers
from .models import User

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
