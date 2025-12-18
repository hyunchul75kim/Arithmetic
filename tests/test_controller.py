"""Controller 테스트"""

import pytest
from src.controller.calculator_controller import CalculatorController
from src.model.calculator_model import CalculatorModel


class TestCalculatorController:
    """CalculatorController 테스트 클래스"""
    
    @pytest.fixture
    def controller(self):
        """컨트롤러 픽스처"""
        model = CalculatorModel()
        return CalculatorController(model)
    
    def test_set_first_number_valid(self, controller):
        """유효한 첫 번째 숫자 설정"""
        success, error = controller.set_first_number("10")
        assert success
        assert error is None
        assert controller.model.first_number == 10.0
    
    def test_set_first_number_invalid(self, controller):
        """유효하지 않은 첫 번째 숫자 설정"""
        success, error = controller.set_first_number("abc")
        assert not success
        assert error is not None
    
    def test_set_operator_valid(self, controller):
        """유효한 연산자 설정"""
        success, error = controller.set_operator("+")
        assert success
        assert error is None
        assert controller.model.operator == "+"
    
    def test_set_operator_invalid(self, controller):
        """유효하지 않은 연산자 설정"""
        success, error = controller.set_operator("@")
        assert not success
        assert error is not None
    
    def test_calculate_success(self, controller):
        """성공적인 계산"""
        controller.set_first_number("10")
        controller.set_operator("+")
        controller.set_second_number("5")
        
        success, result, error = controller.calculate()
        assert success
        assert "10+5=15" in result
        assert error is None
    
    def test_calculate_division_by_zero(self, controller):
        """0으로 나누기 테스트"""
        controller.set_first_number("10")
        controller.set_operator("/")
        controller.set_second_number("0")
        
        success, result, error = controller.calculate()
        assert not success
        assert "0으로 나눌 수 없습니다" in error
    
    def test_reset(self, controller):
        """초기화 테스트"""
        controller.set_first_number("10")
        controller.set_operator("+")
        controller.set_second_number("5")
        
        controller.reset()
        assert controller.model.first_number is None
        assert controller.model.operator is None
        assert controller.model.second_number is None
    
    def test_get_display_value(self, controller):
        """표시 값 가져오기 테스트"""
        # 초기 상태
        assert controller.get_display_value() == "0"
        
        # 첫 번째 숫자 설정 후
        controller.set_first_number("10")
        assert controller.get_display_value() == "10"
        
        # 두 번째 숫자 설정 후
        controller.set_operator("+")
        controller.set_second_number("5")
        assert controller.get_display_value() == "5"
        
        # 계산 후
        controller.calculate()
        assert controller.get_display_value() == "15"

