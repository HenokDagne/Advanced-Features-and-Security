from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CustomUserSerializer, PremiumUserSerializer
from .models import CustomUser, PremiumUser
from django.db.models import Q
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
        return Response({'message': 'User created successfully.'}, status=201)


    


    


