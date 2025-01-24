from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password':{'required':True, 'write_only':True}}

class MealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meals
        fields = ('id', 'name', 'description', 'avg_ratings', 'no_ratungs')


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ('id', 'user', 'meal', 'rating')