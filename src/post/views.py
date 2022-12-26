from django.contrib.auth.models import User
#from django.shortcuts import render
from django.http import Http404
# third party
#from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, mixins, generics

from .serializers import PostSerializer
from .models import Post
from .permissions import IsOwnerOrReadOnly

from user.serializers import UserSerializer


class TestView(APIView):
    """
        Retrieve, update or delete Post
    """
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    
    def get_obj(self, request, pk):
        try:
            obj = Post.objects.get(pk=pk)
            self.check_object_permissions(request, obj)
            return obj
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, *args, **kwargs):
        #qs = Post.objects.all()
        #serializer = PostSerializer(qs, many=True)
        post = self.get_obj(request, pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self, request, pk):
        post = self.get_obj(request, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        post = self.get_obj(request, pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostView(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)


class PostCreateView(mixins.ListModelMixin,
                     generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, request):
        return self.list(request)


class PostListCreateView(mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def put(self, request, **kwargs):
        return self.update(request, **kwargs)
    
    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    

class PostRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostOwnerView(generics.RetrieveAPIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]
    queryset = Post.objects.all()
    serializer_class = UserSerializer
    
    def get_object(self, *args, **kwargs):
        post = super().get_object(*args, **kwargs)
        user = post.owner
        return user
        
