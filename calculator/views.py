import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime


# Переадресация на страницу калькулятора
def redirect_to_calculator(request):
    return redirect('/calculator')

history = []

def validate_operation(first, second, operator):
    try:
        float(first)
        float(second)
    except ValueError:
        return 'Каждое из значений должно быть числом'

    if operator == '/' and float(second) == 0:
        return 'Невозможно выполнить операцию деления на ноль'

    if operator == 'sqrt' and float(first) < 0:
        return 'Невозможно извлечь квадратный корень из отрицательного числа'

def calculate(request):
    data = json.loads(request.body)
    first = data['first']
    second = data['second']
    operator = data['operator']
    result = None

    response_data = {
        'success': False,
        'message': 'Что-то пошло не так',
    }

    error_message = validate_operation(first, second, operator)

    if error_message:
        response_data = {
            'success': False,
            'message': error_message,
        }
    else:
        operation = ' '.join([first, operator, second])
        if operator == '^':
            result = pow(float(first), float(second))
        elif operator == 'sqrt':
            result = pow(float(first), 0.5)

        else:
            result = eval(operation)

        history_line = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + operation + ' = ' + str(result)
        history.insert(0, history_line)
        del history[10:]

        response_data = {
            'success': True,
            'data': {
                'operation': operation + ' =',
                'result': result,
            },
        }

    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json',
        status=200,
    )

def calculator_view(request):
    if request.method == 'POST':
        # Возвращаем кастомный ответ
        return calculate(request)
    else:
        return render(
            request,
            'calculator.html',
            context={},
        )

def history_view(request):
    if request.method == 'DELETE':
        del history[:]

    return render(
        request,
        'history.html',
        context={
            'history': history,
        },
    )