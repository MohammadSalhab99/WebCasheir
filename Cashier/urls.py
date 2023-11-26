from django.urls import path
from . import views
from .views import ProductListCreateView, ProductRetrieveUpdateDeleteView,Pay,TransactionsReport,UserRegistrationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDeleteView.as_view(), name='product-manipulate'),
    path('pay/<int:cashier_id>/', Pay.as_view(), name='pay-api'),
    path('transactions/', TransactionsReport.as_view(), name='transactions-report-api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token generation
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refreshing
    path('api/register/', UserRegistrationView.as_view(), name='user-registration'),


]