"""
간단한 사칙연산 콘솔 프로그램

사용자로부터 두 개의 정수값과 연산자를 입력받아 계산 결과를 출력합니다.
"""

from arithmetic import add, subtract, multiply, divide, quotient


def get_integer_input(prompt: str) -> int:
    """
    사용자로부터 정수값을 입력받습니다.
    
    Args:
        prompt (str): 입력 프롬프트 메시지
    
    Returns:
        int: 입력받은 정수값
    
    Raises:
        ValueError: 유효하지 않은 정수값이 입력된 경우
    """
    while True:
        try:
            value = input(prompt)
            return int(value)
        except ValueError:
            print("올바른 정수값을 입력해주세요.")


def get_operator_input() -> str:
    """
    사용자로부터 연산자를 입력받습니다.
    
    Returns:
        str: 유효한 연산자 (+, -, *, /, //)
    
    Raises:
        ValueError: 유효하지 않은 연산자가 입력된 경우
    """
    valid_operators = ['+', '-', '*', '/', '//']
    while True:
        operator = input("연산자>>")
        if operator in valid_operators:
            return operator
        print(f"올바른 연산자를 입력해주세요. ({', '.join(valid_operators)})")


def calculate(a: int, operator: str, b: int) -> float:
    """
    두 정수와 연산자를 사용하여 계산을 수행합니다.
    
    Args:
        a (int): 첫 번째 정수값
        operator (str): 연산자 (+, -, *, /, //)
        b (int): 두 번째 정수값
    
    Returns:
        float: 계산 결과
    
    Raises:
        ZeroDivisionError: 나눗셈 연산에서 0으로 나누는 경우
        ValueError: 유효하지 않은 연산자인 경우
    """
    if operator == '+':
        return add(a, b)
    elif operator == '-':
        return subtract(a, b)
    elif operator == '*':
        return multiply(a, b)
    elif operator == '/':
        return quotient(a, b)
    elif operator == '//':
        return divide(a, b)
    else:
        raise ValueError(f"지원하지 않는 연산자입니다: {operator}")


def format_result(a: int, operator: str, b: int, result: float) -> str:
    """
    계산 결과를 포맷팅합니다.
    
    Args:
        a (int): 첫 번째 정수값
        operator (str): 연산자
        b (int): 두 번째 정수값
        result (float): 계산 결과
    
    Returns:
        str: 포맷팅된 결과 문자열
    """
    # 정수 결과인 경우 소수점 제거
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    
    return f"{a}{operator}{b}={result}입니다."


def main():
    """메인 함수: 콘솔 프로그램 실행"""
    print("=" * 50)
    print("간단한 사칙연산 콘솔 프로그램")
    print("=" * 50)
    print()
    
    try:
        # 첫 번째 정수값 입력
        a = get_integer_input("첫번째 정수값 >>")
        
        # 연산자 입력
        operator = get_operator_input()
        
        # 두 번째 정수값 입력
        b = get_integer_input("두번째 정수값 >>")
        
        # 계산 수행
        result = calculate(a, operator, b)
        
        # 결과 출력
        print()
        print("=" * 50)
        expression = f"{a}{operator}{b}을 계산합니다."
        print(expression)
        print("=" * 50)
        print(format_result(a, operator, b, result))
        
    except ZeroDivisionError:
        print()
        print("=" * 50)
        print("오류: 0으로 나눌 수 없습니다.")
        print("=" * 50)
    except KeyboardInterrupt:
        print()
        print("\n프로그램이 종료되었습니다.")
    except Exception as e:
        print()
        print("=" * 50)
        print(f"오류가 발생했습니다: {e}")
        print("=" * 50)


if __name__ == "__main__":
    main()

