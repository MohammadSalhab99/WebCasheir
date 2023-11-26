from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone 
# Define a custom user manager for the CustomUser model
class CustomUserManager(BaseUserManager):
    # Create a standard user
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Create a superuser with additional permissions
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # Create the superuser using the create_user method
        return self.create_user(username, password, **extra_fields)

# Define a custom user model
class User(AbstractBaseUser):
    user_name = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    last_login = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self)
    USERNAME_FIELD = 'user_name' 
    # Other fields...
# Define a Product model
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Define a Transaction model
class Transaction(models.Model):
    number_of_items = models.IntegerField()
    cashier = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='TransactionItem')
    transaction_time = models.DateTimeField()

    def __str__(self):
        return f"Transaction #{self.pk} by {self.cashier.user_name}"

# Define a TransactionItem model that represents items in a transaction
class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} {self.item.name}(s) in Transaction #{self.transaction.pk}'