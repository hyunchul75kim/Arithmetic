"""CalculatorModel 테스트"""

import pytest
from src.model.calculator_model import CalculatorModel


class TestCalculatorModel:
    """CalculatorModel 테스트 클래스"""
    
    def test_initial_state(self):
        """초기 상태 테스트"""
        model = CalculatorModel()
        assert model.first_number is None
        assert model.operator is None
        assert model.second_number is None
        assert model.result is None
        assert not model.is_ready_to_calculate()
    
    def test_set_values(self):
        """값 설정 테스트"""
        model = CalculatorModel()
        model.set_first_number(10)
        model.set_operator('+')
        model.set_second_number(5)
        
        assert model.first_number == 10
        assert model.operator == '+'
        assert model.second_number == 5
        assert model.is_ready_to_calculate()
    
    def test_calculate_addition(self):
        """덧셈 계산 테스트"""
        model = CalculatorModel()
        model.set_first_number(10)
        model.set_operator('+')
        model.set_second_number(5)
        
        result = model.calculate()
        assert result == 15
    
    def test_calculate_subtraction(self):
        """뺄셈 계산 테스트"""
        model = CalculatorModel()
        model.set_first_number(10)
        model.set_operator('-')
        model.set_second_number(3)
        
        result = model.calculate()
        assert result == 7
    
    def test_calculate_multiplication(self):
        """곱셈 계산 테스트"""
        model = CalculatorModel()
        model.set_first_number(5)
        model.set_operator('*')
        model.set_second_number(4)
        
        result = model.calculate()
        assert result == 20
    
    def test_calculate_division(self):
        """나눗셈 계산 테스트"""
        model = CalculatorModel()
        model.set_first_number(10)
        model.set_operator('/')
        model.set_second_number(2)
        
        result = model.calculate()
        assert result == 5.0
    
    def test_calculate_integer_division(self):
        """정수 나눗셈 계산 테스트"""
        model = CalculatorModel()
        model.set_first_number(10)
        model.set_operator('//')
        model.set_second_number(3)
        
        result = model.calculate()
        assert result == 3
    
    def test_division_by_zero(self):
        """0으로 나누기 테스트"""
        model = CalculatorModel()
        model.set_first_number(10)
        model.set_operator('/')
        model.set_second_number(0)
        
        with pytest.raises(ZeroDivisionError):
            model.calculate()
    
    def test_reset(self):
        """초기화 테스트"""
        model = CalculatorModel()
        model.set_first_number(10)
        model.set_operator('+')
        model.set_second_number(5)
        model.calculate()
        
        model.reset()
        assert model.first_number is None
        assert model.operator is None
        assert model.second_number is None
        assert model.result is None
    
    def test_invalid_operator(self):
        """유효하지 않은 연산자 테스트"""
        model = CalculatorModel()
        model.set_first_number(10)
        
        with pytest.raises(ValueError):
            model.set_operator('@')

