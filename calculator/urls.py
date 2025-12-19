from django.urls import path
from .views import UserLoginView, UserRegisterView, CalculatorView, CalculateView, OperationsListView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', CalculatorView.as_view(), name='index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('calculate/', CalculateView.as_view(), name='calculate'),
    path('operations/', OperationsListView.as_view(), name='operations_list'),
]