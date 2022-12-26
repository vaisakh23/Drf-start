from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True, source='owner.username')
    class Meta:
        model = Post
        fields = '__all__'

