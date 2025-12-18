"""
객체 생성 팩토리

의존성 주입을 위한 팩토리 클래스입니다.
"""

from src.model.calculator_model import CalculatorModel
from src.controller.calculator_controller import CalculatorController


class CalculatorFactory:
    """계산기 객체 생성 팩토리"""
    
    @staticmethod
    def create_model() -> CalculatorModel:
        """
        CalculatorModel 인스턴스를 생성합니다.
        
        Returns:
            CalculatorModel 인스턴스
        """
        return CalculatorModel()
    
    @staticmethod
    def create_controller(model: CalculatorModel) -> CalculatorController:
        """
        CalculatorController 인스턴스를 생성합니다.
        
        Args:
            model: CalculatorModel 인스턴스
            
        Returns:
            CalculatorController 인스턴스
        """
        return CalculatorController(model)
    
    @staticmethod
    def create_calculator_components() -> tuple[CalculatorModel, CalculatorController]:
        """
        계산기 컴포넌트들을 생성합니다.
        
        Returns:
            (CalculatorModel, CalculatorController) 튜플
        """
        model = CalculatorFactory.create_model()
        controller = CalculatorFactory.create_controller(model)
        return model, controller

