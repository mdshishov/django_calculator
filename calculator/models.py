from django.db import models
from django.contrib.auth.models import User


class Operation(models.Model):
    OPERATOR_CHOICES = {
        'add': '+',
        'sub': '-',
        'mul': '*',
        'div': '/',
    }

    operator = models.CharField(choices=OPERATOR_CHOICES, max_length=5)
    operand1 = models.FloatField()
    operand2 = models.FloatField()
    result = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operations')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.operand1} {self.get_operation_sign()} {self.operand2} = {self.result}'

    def get_operation_sign(self):
        return self.OPERATOR_CHOICES[self.operator]
