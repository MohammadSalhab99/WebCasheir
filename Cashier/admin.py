from django.contrib import admin
from .models import User,Product,Transaction, TransactionItem


admin.site.register(User)

admin.site.register(Product)

admin.site.register(Transaction)

admin.site.register(TransactionItem)
