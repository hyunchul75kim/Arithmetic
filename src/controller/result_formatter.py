"""
결과 포맷팅 모듈

계산 결과를 사용자에게 표시하기 적합한 형식으로 포맷팅합니다.
"""


class ResultFormatter:
    """결과 포맷팅 클래스"""
    
    @staticmethod
    def format_result(a: float, operator: str, b: float, result: float) -> str:
        """
        계산 결과를 포맷팅합니다.
        
        Args:
            a: 첫 번째 숫자
            operator: 연산자
            b: 두 번째 숫자
            result: 계산 결과
            
        Returns:
            포맷팅된 결과 문자열
        """
        # 정수 결과인 경우 소수점 제거
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        
        return f"{a}{operator}{b}={result}입니다."
    
    @staticmethod
    def format_display_number(value: float) -> str:
        """
        표시용 숫자를 포맷팅합니다.
        
        Args:
            value: 숫자 값
            
        Returns:
            포맷팅된 문자열
        """
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)

