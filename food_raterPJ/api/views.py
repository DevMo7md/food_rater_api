from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            token, created= Token.objects.get_or_create(user=user)
            user.save()
            serializer = UserSerializer(user, many=False)
            login(request, user)
            response = {
                'token': token.key,
                'user': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request, pk=None):
    if request.method == 'POST':
        try:
            logout(request)
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user(request, pk=None):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class MealsView(viewsets.ModelViewSet):
    model = Meals
    serializer_class = MealsSerializer
    queryset = Meals.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)


    @action(methods=['PUT', 'POST'], detail=True)
    def add_rate(self, request, pk=None):
        if 'stars' in request.data:
            meal = Meals.objects.get(id=pk)
            stars = request.data.get('stars')
            user = request.user
            if request.method == 'POST':
                rate_obj = Rate.objects.create(meal=meal, user=user, rating=stars)
                
                serializer = RateSerializer(rate_obj, many=False)
                json = {
                    "message": "Meale Rated",
                    "result": serializer.data
                }
                return Response(json, status=status.HTTP_201_CREATED)
            elif request.method == 'PUT':
                rate_obj = Rate.objects.get(meal=meal, user=user)
                rate_obj.rating = stars
                rate_obj.save()
                
                serializer = RateSerializer(rate_obj, many=False)
                json = {
                    "message": "Meale Rate Updated",
                    "result": serializer.data
                }
                return Response(json, status=status.HTTP_201_CREATED)
        else:
            json = {
                "message": "Stars is required",
            }
            return Response(json, status=status.HTTP_400_BAD_REQUEST)

class RateView(viewsets.ModelViewSet):
    model = Rate
    serializer_class = RateSerializer
    queryset = Rate.objects.all()
    authentication_classes = (TokenAuthentication,)