# serializers.py
from rest_framework import serializers
from .models import Product,Transaction,User,CustomUserManager
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
# Transaction Serializer       
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'