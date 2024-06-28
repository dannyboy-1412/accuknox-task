# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate

from social_user.models import User

User = User

class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

