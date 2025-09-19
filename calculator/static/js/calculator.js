const csrftoken = document.getElementById('csrf_token').content;

const formEl = document.getElementById('calculator_form');
const firstEl = formEl.elements.first;
const secondEl = formEl.elements.second;
const operatorEl = formEl.elements.operator;
const submitBtn = formEl.elements.submit_btn;
const errorEl = document.getElementById('error');
const resultContainer = document.getElementById('result_container');
const resultEl = document.getElementById('result');
const operationEl = document.getElementById('operation');

formEl.addEventListener('submit', submitForm);

operatorEl.addEventListener('change', handleOperatorChange);

firstEl.addEventListener('input', validateOnInput);
firstEl.addEventListener('blur', handleOnBlur);

secondEl.addEventListener('input', validateOnInput);
secondEl.addEventListener('blur', handleOnBlur);

updateSubmitBtnDisability()

async function submitForm(e) {
    e.preventDefault();

    const body = {
        first: firstEl.value,
        second: secondEl.value,
        operator: operatorEl.value,
    };
    const url = formEl.getAttribute('action');

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json;charset=utf-8',
        },
        body: JSON.stringify(body)
    });

    responseHandle(response)
}

async function responseHandle(response) {
    errorEl.classList.toggle('hidden', true);
    resultContainer.classList.toggle('hidden', true);

    if (!response.ok) {
        errorEl.innerHTML = '';
        errorEl.append(
            'Ошибка сервера',
            document.createElement('br'),
            `${response.status}: ${response.statusText}`,
        );
        errorEl.classList.toggle('hidden', false);
        return;
    }

    const data = await response.json()

    if (data.success) {
        const {operation, result} = data.data;
        operationEl.textContent = operation;
        resultEl.textContent = result;
        resultContainer.classList.toggle('hidden', false);
        formEl.reset();
        updateSubmitBtnDisability();
    } else {
        errorEl.textContent = data.message;
        errorEl.classList.toggle('hidden', false);
    }
}

function validateOnInput(e) {
    const input = e.target;
    input.value = input.value
        .replace(/[^0-9,.-]/g, '')
        .replace(/,/g, '.')
        .replace('.', '|')
        .replace(/\./g, '')
        .replace('|', '.');

    const isNegative = input.value.startsWith('-');
    const positiveValue = input.value.replace(/-/g, '')
    input.value = (isNegative ? '-' : '')
        + (positiveValue.startsWith('.') ? '0' : '') +
        positiveValue;

    updateSubmitBtnDisability();
}

function handleOnBlur(e) {
    const elem = e.target;

    elem.value = elem.value ? Number(elem.value) : '';

    if (elem.value) {
        elem.classList.toggle('invalid', false);
    } else {
        elem.classList.toggle('invalid', true);
    }

    updateSubmitBtnDisability();
}

function updateSubmitBtnDisability() {
    if (firstEl.value && secondEl.value) {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
}

function handleOperatorChange() {
    if (operatorEl.value === 'sqrt') {
        if (!secondEl.value) secondEl.value = 0;
        secondEl.disabled = true;
    } else {
        secondEl.disabled = false;
    }

    updateSubmitBtnDisability();
}
