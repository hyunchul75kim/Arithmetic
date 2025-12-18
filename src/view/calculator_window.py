"""
계산기 메인 윈도우

PyQt5를 사용한 계산기 GUI 애플리케이션입니다.
"""

from typing import Optional
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from src.view.display_widget import DisplayWidget
from src.view.number_pad import NumberPad
from src.controller.calculator_controller import CalculatorController
from src.model.calculator_model import CalculatorModel
from src.model.operation_strategy import OperationStrategyFactory
from src.factory import CalculatorFactory


class CalculatorWindow(QMainWindow):
    """계산기 메인 윈도우"""
    
    def __init__(self, 
                 model: Optional[CalculatorModel] = None,
                 controller: Optional[CalculatorController] = None):
        """
        계산기 윈도우 초기화
        
        Args:
            model: CalculatorModel 인스턴스 (없으면 Factory로 생성)
            controller: CalculatorController 인스턴스 (없으면 Factory로 생성)
        """
        super().__init__()
        
        # 의존성 주입: Factory 패턴 사용
        if model is None or controller is None:
            self.model, self.controller = CalculatorFactory.create_calculator_components()
        else:
            self.model = model
            self.controller = controller
        
        # 입력 상태 관리
        self._current_input: str = ""
        self._input_state: str = "first"  # "first", "operator", "second"
        
        self._init_ui()
        self._connect_signals()
    
    def _init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("계산기")
        self.setFixedSize(300, 450)
        
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 표시 영역
        self.display = DisplayWidget()
        main_layout.addWidget(self.display)
        
        # 숫자 키패드
        self.number_pad = NumberPad()
        main_layout.addWidget(self.number_pad)
        
        # 연산자 버튼
        operator_layout = QHBoxLayout()
        operator_layout.setSpacing(5)
        
        operators = OperationStrategyFactory.get_supported_operators()
        
        for op in operators:
            btn = self._create_operator_button(op)
            operator_layout.addWidget(btn)
            btn.clicked.connect(lambda checked, o=op: self._on_operator_clicked(o))
        
        main_layout.addLayout(operator_layout)
        
        # 계산 및 초기화 버튼
        action_layout = QHBoxLayout()
        action_layout.setSpacing(5)
        
        calc_btn = QPushButton("=")
        calc_btn.setMinimumHeight(50)
        calc_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        calc_btn.clicked.connect(self._on_calculate_clicked)
        
        reset_btn = QPushButton("C")
        reset_btn.setMinimumHeight(50)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        reset_btn.clicked.connect(self._on_reset_clicked)
        
        action_layout.addWidget(calc_btn)
        action_layout.addWidget(reset_btn)
        
        main_layout.addLayout(action_layout)
        
        central_widget.setLayout(main_layout)
    
    def _create_operator_button(self, text: str) -> QPushButton:
        """
        연산자 버튼 생성
        
        Args:
            text: 버튼에 표시할 텍스트
            
        Returns:
            생성된 QPushButton 인스턴스
        """
        btn = QPushButton(text)
        btn.setMinimumSize(50, 50)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        return btn
    
    def _connect_signals(self):
        """시그널 연결"""
        self.number_pad.number_clicked.connect(self._on_number_clicked)
        self.number_pad.dot_clicked.connect(self._on_dot_clicked)
        self.number_pad.sign_clicked.connect(self._on_sign_clicked)
    
    def _on_number_clicked(self, number: str) -> None:
        """
        숫자 버튼 클릭 처리
        
        Args:
            number: 클릭된 숫자 문자열
        """
        if self._input_state == "first":
            if self._current_input == "0":
                self._current_input = number
            else:
                self._current_input += number
            
            success, error = self.controller.set_first_number(self._current_input)
            if success:
                self.display.set_value(self._current_input)
            else:
                self._show_error(error or "올바른 숫자를 입력해주세요.")
                    
        elif self._input_state == "second":
            if self._current_input == "0":
                self._current_input = number
            else:
                self._current_input += number
            
            success, error = self.controller.set_second_number(self._current_input)
            if success:
                self.display.set_value(self._current_input)
            else:
                self._show_error(error or "올바른 숫자를 입력해주세요.")
    
    def _on_dot_clicked(self) -> None:
        """소수점 버튼 클릭 처리"""
        if '.' not in self._current_input:
            if not self._current_input:
                self._current_input = "0."
            else:
                self._current_input += '.'
            
            if self._input_state in ("first", "second"):
                self.display.set_value(self._current_input)
    
    def _on_sign_clicked(self) -> None:
        """+/- 버튼 클릭 처리"""
        if self._current_input and self._current_input != "0":
            if self._current_input.startswith('-'):
                self._current_input = self._current_input[1:]
            else:
                self._current_input = '-' + self._current_input
            
            if self._input_state == "first":
                success, error = self.controller.set_first_number(self._current_input)
                if success:
                    self.display.set_value(self._current_input)
            elif self._input_state == "second":
                success, error = self.controller.set_second_number(self._current_input)
                if success:
                    self.display.set_value(self._current_input)
    
    def _on_operator_clicked(self, operator: str) -> None:
        """
        연산자 버튼 클릭 처리
        
        Args:
            operator: 선택된 연산자
        """
        if self._input_state == "first":
            success, error = self.controller.set_operator(operator)
            if success:
                self._input_state = "operator"
                self._current_input = ""
            else:
                self._show_error(error or "연산자를 설정할 수 없습니다.")
        elif self._input_state == "operator":
            # 연산자 변경
            success, error = self.controller.set_operator(operator)
            if not success:
                self._show_error(error or "연산자를 변경할 수 없습니다.")
        elif self._input_state == "second":
            # 두 번째 숫자가 입력된 상태에서 연산자 클릭 시 계산 후 연산자 변경
            self._perform_calculation()
            success, error = self.controller.set_operator(operator)
            if success:
                self._input_state = "operator"
                self._current_input = ""
    
    def _on_calculate_clicked(self) -> None:
        """계산 버튼 클릭 처리"""
        self._perform_calculation()
    
    def _perform_calculation(self) -> None:
        """계산 수행"""
        if self.controller.model.is_ready_to_calculate():
            success, result, error = self.controller.calculate()
            if success:
                self.display.set_value(self.controller.get_display_value())
                # 결과를 첫 번째 숫자로 설정하여 연속 계산 가능
                self._input_state = "first"
                self._current_input = ""
            else:
                self._show_error(error or "계산 중 오류가 발생했습니다.")
        else:
            self._show_error("계산할 수 없습니다. 모든 값을 입력해주세요.")
    
    def _on_reset_clicked(self) -> None:
        """초기화 버튼 클릭 처리"""
        self.controller.reset()
        self._current_input = ""
        self._input_state = "first"
        self.display.set_value("0")
    
    def _show_error(self, message: str) -> None:
        """
        에러 메시지 표시
        
        Args:
            message: 에러 메시지
        """
        if message:
            QMessageBox.warning(self, "오류", message)

