#계산기
def add(a,b):
    reteun a + b
def substract(a,b):
    reteun a - b
def multiply(a,b):
    reteun a * b
def divide(a,b):
    reteun a / b
    if b == 0
    return "Error"
while True:
    choice = input("연산을 선택(+,-,/),종료(q)")
    if choice == 'q':
        break

    num = float(input("숫자1:"))
    num = float(input("숫자2:"))

    if choice =='+':
        print(add(num1,num2))
    elif choice == "-":
        print(substract(num1,num2))
    elif choice == "*":
        print(multiply(num1,num2))
    elif choice == "/":
        print(divide(num1,num2))
    else:
        print("잘못된 연산자입니다.")