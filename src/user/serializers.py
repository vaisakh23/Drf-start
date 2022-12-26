from django.contrib.auth.models import User
from rest_framework import serializers
from post.serializers import PostSerializer


class UserSerializer(serializers.ModelSerializer):
    #post_set = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    post_set = PostSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'post_set'
        ]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=140)
    email = serializers.EmailField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    
    def validate_username(self, username):
        user = User.objects.filter(username=username)
        if user:
            raise serializers.ValidationError("Username already registered.")
        return username
    
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Password doesn't match.")
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'], 
            email=validated_data.get('email')
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
    
