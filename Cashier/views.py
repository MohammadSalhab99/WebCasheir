from django.shortcuts import render
from .models import User, Product, Transaction, TransactionItem
from .serializers import ProductSerializer, TransactionSerializer,TokenObtainPairSerializer
from rest_framework import generics, status,permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView

# View for listing and creating products
class ProductListCreateView(generics.ListCreateAPIView):
    # Retrieve all products
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Create a new product
        serializer.save()
    
# View for retrieving, updating, and deleting products
class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve all products
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]

# View for processing a payment and creating a transaction
class Pay(APIView):
    def post(self, request, cashier_id):
        cashier_id = int(cashier_id)
        items = request.data.get('items')
        num_of_items = 0

        # Calculate the total number of items in the transaction
        for item in items:
            num_of_items += item['qty']

        # Retrieve the cashier user
        cashier = User.objects.get(id=cashier_id)

        # Create a new transaction
        transaction = Transaction(number_of_items=num_of_items, cashier=cashier, transaction_time=datetime.now())
        transaction.save()

        # Create related TransactionItem objects
        for item in items:
            product = Product.objects.get(id=item['id'])
            TransactionItem(transaction=transaction, quantity=item['qty'], item=product)

        return Response("success")

# View for retrieving transactions
class TransactionsReport(APIView):
    def get(self, request):
        # Retrieve all transactions
        queryset = Transaction.objects.all()
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    
from .serializers import UserSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()