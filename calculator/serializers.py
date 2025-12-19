from rest_framework import serializers
from .models import Operation
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False, 'allow_null': True},
            'username': {'validators': []},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Пользователь с таким именем уже существует')
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except:
            raise serializers.ValidationError('Слишком короткий пароль')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'
        read_only_fields = ('id', 'result', 'created_at', 'user')

    def validate(self, data):
        operator = data['operator']
        operand2 = data['operand2']

        if operator == 'div' and operand2 == 0:
            raise serializers.ValidationError('Невозможно поделить на 0')

        if operator not in Operation.OPERATOR_CHOICES:
            raise serializers.ValidationError('Некорректный оператор')

        return data

    def create(self, validated_data):
        operator = validated_data['operator']
        operand1 = validated_data['operand1']
        operand2 = validated_data['operand2']

        result = None
        if operator == 'add':
            result = operand1 + operand2
        elif operator == 'sub':
            result = operand1 - operand2
        elif operator == 'mul':
            result = operand1 * operand2
        elif operator == 'div':
            result = operand1 / operand2

        user = self.context['request'].user

        operation = Operation.objects.create(
            result=result,
            user=user,
            **validated_data,
        )
        return operation

