from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import CustomUser, Blog
from django.contrib.auth import get_user_model



class UpdateUserProfileSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'bio', 'job_title', 'profilepic', 'facebook', 'youtube', 'instagram' , 'twitter']


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        #email = validated_data['email']
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data['password']

        user = get_user_model()
        new_user = user.objects.create(username = username, first_name = first_name, last_name= last_name)
        new_user.set_password(password)
        new_user.save()
        return new_user
    

class SimpleAuthorSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name','profilepic']

class BlogSerializer(ModelSerializer):
    author = SimpleAuthorSerializer(read_only=True)
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'author', 'category', 'content', 'featured_img', 'published_date', 'created_at', 'updated_at', 'is_draft']


class UserInfoSerializer(ModelSerializer):
    author_posts = SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "first_name", "last_name", "job_title", "bio", "profilepic", "facebook", "youtube",
            "instagram", "twitter", "author_posts"]

    
    def get_author_posts(self, user):
        blogs = Blog.objects.filter(author=user)[:9]
        serializer = BlogSerializer(blogs, many=True)
        return serializer.data