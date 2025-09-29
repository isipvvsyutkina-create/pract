op = input("Введите оператор: ")
if op in["and", "or", "not"] :
    a = input("Введите первое значение:")
    a = True if a == "True" else False
    if op == "not":
      result = not a
    else:
        b = input("Введите второе значение: ")
        b = True if b == "True" else False
    if op == "and":
        result = a and b
    elif op == "or":
        result = a or b
else:
    a = float(input("Введите первое число: "))
    b = float(input("Введите второе число: "))

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    elif op == "/":
        if b != 0:
            result = a / b
        else:
            result = "Ошибка: деление на ноль!"
    elif op == "//":
        if b != 0:
            result = a // b
        else:
            result = "Ошибка: деление на ноль!"
    elif op == "%":
        if b != 0:
            result = a % b
        else:
            result = "Ошибка: деление на ноль!"
    elif op == "**":
        result = a ** b
    elif op == "==":
        result = a == b
    elif op == "!=":
        result = a != b
    elif op == ">":
        result = a > b
    elif op == "<":
        result = a < b
    elif op == ">=":
        result = a >= b
    elif op == "<=":
        result = a <= b
    else:
        result = "Неизвестный оператор!"

print("Результат:", result)

