"""
사칙연산 정확도 테스트 케이스
TC-CMM-001 / TC-AO-001
"""

import pytest
from src.arithmetic import add, subtract, multiply, divide, quotient


class TestAddition:
    """덧셈 테스트"""
    
    def test_add_1_and_10(self):
        """1 + 10 = 11"""
        assert add(1, 10) == 11
    
    def test_add_0_and_1(self):
        """0 + 1 = 1"""
        assert add(0, 1) == 1
    
    def test_add_negative_numbers(self):
        """-1 + (-10) = -11"""
        assert add(-1, -10) == -11


class TestSubtraction:
    """뺄셈 테스트"""
    
    def test_subtract_5_and_2(self):
        """5 - 2 = 3"""
        assert subtract(5, 2) == 3


class TestMultiplication:
    """곱셈 테스트"""
    
    def test_multiply_negative_numbers(self):
        """-5 * -3 = 15"""
        assert multiply(-5, -3) == 15
    
    def test_multiply_by_zero(self):
        """0 * 10 = 0"""
        assert multiply(0, 10) == 0


class TestDivision:
    """나눗셈 테스트"""
    
    def test_divide_5_by_2_integer(self):
        """5 / 2 = 2 (정수 나눗셈)"""
        assert divide(5, 2) == 2
    
    def test_divide_negative_by_positive(self):
        """-10 / 2 = -5"""
        assert divide(-10, 2) == -5
    
    def test_divide_by_zero_exception(self):
        """0 / 0 → ZeroDivisionError 예외 발생"""
        with pytest.raises(ZeroDivisionError):
            divide(0, 0)


class TestQuotient:
    """몫 계산 테스트"""
    
    def test_quotient_5_by_2(self):
        """5 ÷ 2 = 2.5 (몫 계산)"""
        assert quotient(5, 2) == 2.5

