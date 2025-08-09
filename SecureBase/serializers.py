from rest_framework import serializers
from .models import CustomUser, PremiumUser, Post
from datetime import date

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name','password', 'bio', 'profile_picture', 'birth_date', 'age', 'is_premium'
        ]

class PremiumUserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = PremiumUser
        fields = [
            'id', 'user', 'membrership_start_date', 'membership_end_date', 'premium_features_enabled'
        ]


class AuthorSerialize(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'id', 'username', 'email']

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerialize(read_only=True)
    post_time = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'created_at', 'updated_at', 'post_time', 'image', 'user'
        ]
    def validate(self, data):
        if not data.get('content') and not data.get('image'):
            raise serializers.ValidationError("You must provide either content or an image (or both) for a post.") 
        return data   

    def get_post_time(self, obj):
        if obj.created_at:
            days = (date.today() - obj.created_at.date()).days
            if days == 0:
                return "Today"
            elif days == 1:
                return "Yesterday"
            elif days < 7:
                return f"{days} days ago"
            elif days < 30:
                weeks = days // 7
                return f"{weeks} week{'s' if weeks > 1 else ''} ago"
            elif days < 365:
                months = days // 30
                return f"{months} month{'s' if months > 1 else ''} ago"
            else:
                years = days // 365
                return f"{years} year{'s' if years > 1 else ''} ago"
        return None