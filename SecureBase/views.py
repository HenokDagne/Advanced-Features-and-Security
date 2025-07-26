from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CustomUserSerializer, PremiumUserSerializer
from .models import CustomUser, PremiumUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from django.contrib.auth import authenticate
# Create your views here.

class CustomUserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing CustomUser instances.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False, methods=['POST'], url_path='signup')
    def signup(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        if not username or not email or not password or not first_name or not last_name:
            return Response({'errormessage': 'All fields are required.'}, status=400)
        user = CustomUser.objects.filter(Q(username=username) | Q(email=email)).first()
        if user:
            return Response({'errormessage': 'User with this username or email already exists.'}, status=400)
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password, 
            first_name=first_name,
            last_name=last_name
        )
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User created successfully.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=201)
    @action(detail=False, methods=['POST'], url_path='login')
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'errormessage': 'Email and password are required.'}, status=400)
        try:
            user = get_object_or_404(CustomUser, email=email)
            username = user.username
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({'errormessage': 'Invalid credentials.'}, status=400)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=200)
        except CustomUser.DoesNotExist:
            return Response({'errormessage': 'User does not exist.'}, status=404)
             
            
        


    


    


