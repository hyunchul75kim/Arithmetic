"""
계산기 모델

계산기의 상태를 관리하고 계산을 수행합니다.
비즈니스 로직만 담당하며 UI와 독립적입니다.
"""

from typing import Optional
from src.model.operation_strategy import OperationStrategyFactory


class CalculatorModel:
    """계산기 모델 클래스"""
    
    def __init__(self):
        """계산기 모델 초기화"""
        self._first_number: Optional[float] = None
        self._operator: Optional[str] = None
        self._second_number: Optional[float] = None
        self._result: Optional[float] = None
    
    @property
    def first_number(self) -> Optional[float]:
        """첫 번째 숫자"""
        return self._first_number
    
    @property
    def operator(self) -> Optional[str]:
        """연산자"""
        return self._operator
    
    @property
    def second_number(self) -> Optional[float]:
        """두 번째 숫자"""
        return self._second_number
    
    @property
    def result(self) -> Optional[float]:
        """계산 결과"""
        return self._result
    
    def set_first_number(self, value: float) -> None:
        """
        첫 번째 숫자를 설정합니다.
        
        Args:
            value: 첫 번째 숫자 값
        """
        self._first_number = value
        self._result = None
    
    def set_operator(self, operator: str) -> None:
        """
        연산자를 설정합니다.
        
        Args:
            operator: 연산자 (+, -, *, /, //)
            
        Raises:
            ValueError: 지원하지 않는 연산자인 경우
        """
        if operator not in OperationStrategyFactory.get_supported_operators():
            raise ValueError(f"지원하지 않는 연산자입니다: {operator}")
        self._operator = operator
        self._result = None
    
    def set_second_number(self, value: float) -> None:
        """
        두 번째 숫자를 설정합니다.
        
        Args:
            value: 두 번째 숫자 값
        """
        self._second_number = value
        self._result = None
    
    def calculate(self) -> float:
        """
        계산을 수행합니다.
        
        Returns:
            계산 결과
            
        Raises:
            ValueError: 필요한 값이 설정되지 않은 경우
            ZeroDivisionError: 0으로 나누는 경우
        """
        if self._first_number is None:
            raise ValueError("첫 번째 숫자가 설정되지 않았습니다.")
        if self._operator is None:
            raise ValueError("연산자가 설정되지 않았습니다.")
        if self._second_number is None:
            raise ValueError("두 번째 숫자가 설정되지 않았습니다.")
        
        strategy = OperationStrategyFactory.get_strategy(self._operator)
        self._result = strategy.execute(self._first_number, self._second_number)
        return self._result
    
    def reset(self) -> None:
        """계산기 상태를 초기화합니다."""
        self._first_number = None
        self._operator = None
        self._second_number = None
        self._result = None
    
    def is_ready_to_calculate(self) -> bool:
        """
        계산 준비가 되었는지 확인합니다.
        
        Returns:
            계산 준비 여부
        """
        return (
            self._first_number is not None
            and self._operator is not None
            and self._second_number is not None
        )

