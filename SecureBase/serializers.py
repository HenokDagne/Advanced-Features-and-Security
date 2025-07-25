from rest_framework import serializers
from .models import CustomUser, PremiumUser

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
