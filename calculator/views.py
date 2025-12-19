from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect

from .permissions import AllowNonAuthorized
from .serializers import UserSerializer, OperationSerializer
from django.shortcuts import render


class UserRegisterView(APIView):
    permission_classes = (AllowNonAuthorized,)

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                },
            }, status=status.HTTP_201_CREATED)

        return Response(
            {'error': list(serializer.errors.values())[0]},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserLoginView(APIView):
    permission_classes = (AllowNonAuthorized,)

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Поля логин и пароль должны быть заполнены'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {'error': 'Неправильные логин или пароль'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'username': user.username,
            }
        })


class CalculatorView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return render(request, 'calculator.html')

    def handle_exception(self, exc):
        return redirect('login')

class CalculateView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = OperationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            operation = serializer.save()

            return Response({
                    'operator': operation.operator,
                    'operand1': operation.operand1,
                    'operand2': operation.operand2,
                    'result': operation.result,
            }, status=status.HTTP_201_CREATED)

        return Response(
            {'error': list(serializer.errors.values())[0]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def handle_exception(self, exc):
        return redirect('login')

class OperationsListView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if self.request.user.is_superuser:
            operations = User.objects.all()
        else:
            operations = User.objects.filter(user=self.request.user)

        return render(request, 'history.html', {
            'operations': operations,
            'is_superuser': self.request.user.is_superuser,
        })

    def handle_exception(self, exc):
        return redirect('login')