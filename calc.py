# 계산기

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        print("0으로 나눌 수 없습니다.")
        return None
    return a / b


while True:
    choice = input("연산을 선택(+,-,*,/), 종료(q): ")

    if choice == 'q':
        print("계산기를 종료합니다.")
        break

    if choice not in ['+', '-', '*', '/']:
        print("잘못된 연산자입니다.")
        continue

    num1 = float(input("숫자1: "))
    num2 = float(input("숫자2: "))

    if choice == '+':
        print(add(num1, num2))
    elif choice == '-':
        print(subtract(num1, num2))
    elif choice == '*':
        print(multiply(num1, num2))
    elif choice == '/':
        result = divide(num1, num2)
        print(result)
    else:
        print("잘못된 연산자입니다.")
