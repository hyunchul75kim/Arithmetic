"""
입력 검증 모듈

사용자 입력을 검증하고 에러 메시지를 생성합니다.
"""

from typing import Optional


class InputValidator:
    """입력 검증 클래스"""
    
    @staticmethod
    def validate_number(value: str) -> tuple[bool, Optional[float], Optional[str]]:
        """
        숫자 입력을 검증합니다.
        
        Args:
            value: 입력된 문자열
            
        Returns:
            (유효성, 변환된 숫자, 에러 메시지) 튜플
        """
        if not value.strip():
            return False, None, "값을 입력해주세요."
        
        try:
            # 정수 또는 실수로 변환 시도
            if '.' in value:
                number = float(value)
            else:
                number = int(value)
            return True, float(number), None
        except ValueError:
            return False, None, "올바른 숫자를 입력해주세요."
    
    @staticmethod
    def validate_operator(operator: str, supported_operators: list[str]) -> tuple[bool, Optional[str]]:
        """
        연산자 입력을 검증합니다.
        
        Args:
            operator: 입력된 연산자
            supported_operators: 지원하는 연산자 목록
            
        Returns:
            (유효성, 에러 메시지) 튜플
        """
        if operator not in supported_operators:
            operators_str = ', '.join(supported_operators)
            return False, f"올바른 연산자를 입력해주세요. ({operators_str})"
        return True, None

