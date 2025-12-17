"""
사칙연산 모듈

이 모듈은 기본적인 사칙연산(덧셈, 뺄셈, 곱셈, 나눗셈)을 제공합니다.

테스트 ID: TC-CMM-001 (Common Module) / TC-AO-001 (Arithmetic Operations)

제공 함수:
    - add: 덧셈
    - subtract: 뺄셈
    - multiply: 곱셈
    - divide: 정수 나눗셈
    - quotient: 소수점 포함 나눗셈
"""


def add(a: int | float, b: int | float) -> int | float:
    """
    두 숫자의 덧셈을 수행합니다.
    
    Args:
        a (int | float): 첫 번째 숫자
        b (int | float): 두 번째 숫자
    
    Returns:
        int | float: 두 숫자의 합
    
    Examples:
        >>> add(1, 10)
        11
        >>> add(-1, -10)
        -11
        >>> add(0, 1)
        1
    """
    return a + b

def subtract(a: int | float, b: int | float) -> int | float:
    """
    두 숫자의 뺄셈을 수행합니다.
    
    Args:
        a (int | float): 피감수 (빼는 수)
        b (int | float): 감수 (빼어지는 수)
    
    Returns:
        int | float: a에서 b를 뺀 결과
    
    Examples:
        >>> subtract(5, 2)
        3
        >>> subtract(10, -5)
        15
        >>> subtract(0, 10)
        -10
    """
    return a - b

def multiply(a: int | float, b: int | float) -> int | float:
    """
    두 숫자의 곱셈을 수행합니다.
    
    Args:
        a (int | float): 첫 번째 숫자
        b (int | float): 두 번째 숫자
    
    Returns:
        int | float: 두 숫자의 곱
    
    Examples:
        >>> multiply(-5, -3)
        15
        >>> multiply(0, 10)
        0
        >>> multiply(2, 3)
        6
    """
    return a * b

def divide(a: int | float, b: int | float) -> int:
    """
    두 숫자의 정수 나눗셈을 수행합니다.
    
    소수점 이하는 버림 처리됩니다 (// 연산자 사용).
    
    Args:
        a (int | float): 피제수 (나누어지는 수)
        b (int | float): 제수 (나누는 수)
    
    Returns:
        int: a를 b로 나눈 정수 몫
    
    Raises:
        ZeroDivisionError: b가 0일 때 발생
    
    Examples:
        >>> divide(5, 2)
        2
        >>> divide(-10, 2)
        -5
        >>> divide(0, 5)
        0
    """
    if b == 0:
        raise ZeroDivisionError
    return a // b

def quotient(a: int | float, b: int | float) -> float:
    """
    두 숫자의 나눗셈을 수행합니다 (소수점 포함).
    
    정확한 나눗셈 결과를 반환합니다 (/ 연산자 사용).
    
    Args:
        a (int | float): 피제수 (나누어지는 수)
        b (int | float): 제수 (나누는 수)
    
    Returns:
        float: a를 b로 나눈 결과 (소수점 포함)
    
    Raises:
        ZeroDivisionError: b가 0일 때 발생
    
    Examples:
        >>> quotient(5, 2)
        2.5
        >>> quotient(-10, 2)
        -5.0
        >>> quotient(0, 5)
        0.0
    """
    if b == 0:
        raise ZeroDivisionError
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

