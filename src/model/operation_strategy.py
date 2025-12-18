"""
연산 전략 패턴 구현

Strategy Pattern을 사용하여 각 연산을 독립적인 전략으로 분리합니다.
OCP 원칙을 준수하여 새로운 연산자 추가 시 기존 코드 수정 없이 확장 가능합니다.
"""

from typing import Protocol
from src.arithmetic import add, subtract, multiply, divide, quotient


class OperationStrategy(Protocol):
    """연산 전략 프로토콜"""
    
    def execute(self, a: float, b: float) -> float:
        """
        연산을 수행합니다.
        
        Args:
            a: 첫 번째 피연산자
            b: 두 번째 피연산자
            
        Returns:
            계산 결과
            
        Raises:
            ZeroDivisionError: 나눗셈 연산에서 0으로 나누는 경우
        """
        ...


class AddStrategy:
    """덧셈 전략"""
    
    def execute(self, a: float, b: float) -> float:
        return add(a, b)


class SubtractStrategy:
    """뺄셈 전략"""
    
    def execute(self, a: float, b: float) -> float:
        return subtract(a, b)


class MultiplyStrategy:
    """곱셈 전략"""
    
    def execute(self, a: float, b: float) -> float:
        return multiply(a, b)


class DivideStrategy:
    """정수 나눗셈 전략"""
    
    def execute(self, a: float, b: float) -> float:
        return divide(a, b)


class QuotientStrategy:
    """소수점 나눗셈 전략"""
    
    def execute(self, a: float, b: float) -> float:
        return quotient(a, b)


class OperationStrategyFactory:
    """연산 전략 팩토리"""
    
    _strategies = {
        '+': AddStrategy(),
        '-': SubtractStrategy(),
        '*': MultiplyStrategy(),
        '/': QuotientStrategy(),
        '//': DivideStrategy(),
    }
    
    @classmethod
    def get_strategy(cls, operator: str) -> OperationStrategy:
        """
        연산자에 해당하는 전략을 반환합니다.
        
        Args:
            operator: 연산자 (+, -, *, /, //)
            
        Returns:
            해당하는 OperationStrategy 인스턴스
            
        Raises:
            ValueError: 지원하지 않는 연산자인 경우
        """
        if operator not in cls._strategies:
            raise ValueError(f"지원하지 않는 연산자입니다: {operator}")
        return cls._strategies[operator]
    
    @classmethod
    def get_supported_operators(cls) -> list[str]:
        """
        지원하는 연산자 목록을 반환합니다.
        
        Returns:
            지원하는 연산자 목록
        """
        return list(cls._strategies.keys())

