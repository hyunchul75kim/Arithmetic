"""
계산기 컨트롤러

View와 Model 사이를 중재하며, 입력 검증과 결과 포맷팅을 처리합니다.
"""

from typing import Optional
from src.model.calculator_model import CalculatorModel
from src.model.operation_strategy import OperationStrategyFactory
from src.controller.input_validator import InputValidator
from src.controller.result_formatter import ResultFormatter


class CalculatorController:
    """계산기 컨트롤러 클래스"""
    
    def __init__(self, model: CalculatorModel):
        """
        컨트롤러 초기화
        
        Args:
            model: CalculatorModel 인스턴스
        """
        self.model = model
        self.validator = InputValidator()
        self.formatter = ResultFormatter()
    
    def set_first_number(self, value: str) -> tuple[bool, Optional[str]]:
        """
        첫 번째 숫자를 설정합니다.
        
        Args:
            value: 입력된 문자열
            
        Returns:
            (성공 여부, 에러 메시지) 튜플
        """
        is_valid, number, error = self.validator.validate_number(value)
        if is_valid:
            self.model.set_first_number(number)
            return True, None
        return False, error
    
    def set_operator(self, operator: str) -> tuple[bool, Optional[str]]:
        """
        연산자를 설정합니다.
        
        Args:
            operator: 입력된 연산자
            
        Returns:
            (성공 여부, 에러 메시지) 튜플
        """
        supported_operators = OperationStrategyFactory.get_supported_operators()
        is_valid, error = self.validator.validate_operator(operator, supported_operators)
        if is_valid:
            try:
                self.model.set_operator(operator)
                return True, None
            except ValueError as e:
                return False, str(e)
        return False, error
    
    def set_second_number(self, value: str) -> tuple[bool, Optional[str]]:
        """
        두 번째 숫자를 설정합니다.
        
        Args:
            value: 입력된 문자열
            
        Returns:
            (성공 여부, 에러 메시지) 튜플
        """
        is_valid, number, error = self.validator.validate_number(value)
        if is_valid:
            self.model.set_second_number(number)
            return True, None
        return False, error
    
    def calculate(self) -> tuple[bool, Optional[str], Optional[str]]:
        """
        계산을 수행합니다.
        
        Returns:
            (성공 여부, 결과 문자열, 에러 메시지) 튜플
        """
        try:
            result = self.model.calculate()
            a = self.model.first_number
            op = self.model.operator
            b = self.model.second_number
            
            if a is not None and op is not None and b is not None:
                result_str = self.formatter.format_result(a, op, b, result)
                return True, result_str, None
            else:
                return False, None, "계산할 수 없습니다. 모든 값을 입력해주세요."
        except ZeroDivisionError:
            return False, None, "오류: 0으로 나눌 수 없습니다."
        except ValueError as e:
            return False, None, f"오류: {str(e)}"
        except Exception as e:
            return False, None, f"오류가 발생했습니다: {str(e)}"
    
    def reset(self) -> None:
        """계산기를 초기화합니다."""
        self.model.reset()
    
    def get_display_value(self) -> str:
        """
        현재 표시할 값을 반환합니다.
        
        Returns:
            표시할 문자열
        """
        if self.model.result is not None:
            return self.formatter.format_display_number(self.model.result)
        elif self.model.second_number is not None:
            return self.formatter.format_display_number(self.model.second_number)
        elif self.model.first_number is not None:
            return self.formatter.format_display_number(self.model.first_number)
        return "0"

