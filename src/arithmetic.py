"""
사칙연산 모듈
TC-CMM-001 / TC-AO-001
"""

# GREEN 단계: 최소한의 코드로 테스트 통과
def add(a, b):
    """덧셈 함수"""
    return a + b

def subtract(a, b):
    """뺄셈 함수"""
    return a - b

def multiply(a, b):
    """곱셈 함수"""
    return a * b

def divide(a, b):
    """나눗셈 함수 (정수 나눗셈)"""
    if b == 0:
        raise ZeroDivisionError
    return a // b

def quotient(a, b):
    """몫 계산 함수 (소수점 포함)"""
    return a / b


if __name__ == "__main__":
    """모듈을 직접 실행할 때 예제 결과 출력"""
    print("=" * 50)
    print("사칙연산 모듈 실행 예제")
    print("=" * 50)
    print()
    
    # 덧셈 예제
    print("1. 덧셈 (add)")
    print(f"   add(1, 10) = {add(1, 10)}")
    print(f"   add(0, 1) = {add(0, 1)}")
    print(f"   add(-1, -10) = {add(-1, -10)}")
    print()
    
    # 뺄셈 예제
    print("2. 뺄셈 (subtract)")
    print(f"   subtract(5, 2) = {subtract(5, 2)}")
    print()
    
    # 곱셈 예제
    print("3. 곱셈 (multiply)")
    print(f"   multiply(-5, -3) = {multiply(-5, -3)}")
    print(f"   multiply(0, 10) = {multiply(0, 10)}")
    print()
    
    # 나눗셈 예제
    print("4. 나눗셈 (divide - 정수 나눗셈)")
    print(f"   divide(5, 2) = {divide(5, 2)}")
    print(f"   divide(-10, 2) = {divide(-10, 2)}")
    try:
        divide(0, 0)
    except ZeroDivisionError:
        print(f"   divide(0, 0) = ZeroDivisionError 발생")
    print()
    
    # 몫 계산 예제
    print("5. 몫 계산 (quotient - 소수점 포함)")
    print(f"   quotient(5, 2) = {quotient(5, 2)}")
    print()
    
    print("=" * 50)
    print("모든 함수가 정상적으로 동작합니다!")
    print("=" * 50)

