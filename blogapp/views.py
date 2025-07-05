from django.shortcuts import render
from .serializers import UserRegistrationSerializer, BlogSerializer, UpdateUserProfileSerializer, UserInfoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Blog
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
# Create your views here.

class BlogPagination(PageNumberPagination):
    page_size = 3


@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    serialized = UpdateUserProfileSerializer(request.user, data = request.data)
    if serialized.is_valid():
        print("Facebook:", request.data.get("facebook"))
        print("Instagram:", request.data.get("instagram"))

        serialized.save()
        return Response(serialized.data)
    return Response(serialized.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blog(request):
    print("DEBUG request.data:", request.data) 

    serialized = BlogSerializer(data=request.data)
    if serialized.is_valid():
        blog = serialized.save(author=request.user)
        return Response(BlogSerializer(blog).data)
    
    print("DEBUG serializer errors:", serialized.errors) 
    return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'OPTIONS'])
def blog_list(request):
    if request.method == 'OPTIONS':
        return Response(status=status.HTTP_200_OK)

    blogs = Blog.objects.all()
    paginator = BlogPagination()
    paginated_blog = paginator.paginate_queryset(blogs, request)
    serialized = BlogSerializer(paginated_blog, many=True)
    return paginator.get_paginated_response(serialized.data)


@api_view(['GET'])
def get_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    serializer = BlogSerializer(blog)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_blog(request, pk):
    blog = Blog.objects.get(pk = pk)
    if blog.author != request.user:
        return Response({'error':'Not the author for this blog'}, status = status.HTTP_403_FORBIDDEN)
    serialized = BlogSerializer(blog, data = request.data)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data)
    return Response(serialized.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_blog(request, pk):
    blog = Blog.objects.get(pk = pk)
    if request.user == blog.author:
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'error':'Not the author for this blog'}, status = status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_username(request):
    username = request.user.username
    return Response({'username': username})

@api_view(['GET'])
def get_userinfo(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)
    serializer = UserInfoSerializer(user)
    return Response(serializer.data)
