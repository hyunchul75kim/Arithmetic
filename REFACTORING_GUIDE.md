# PyQt GUI 리팩토링 단계별 구현 가이드

## 개요

이 문서는 콘솔 계산기 프로그램을 PyQt GUI 프로그램으로 리팩토링하는 상세한 단계별 가이드를 제공합니다.

---

## 사전 준비

### 1. PyQt5 설치

```bash
pip install PyQt5
```

### 2. requirements.txt 업데이트

```txt
pytest>=7.0.0
pytest-cov>=4.0.0
PyQt5>=5.15.0
```

---

## Phase 1: 모델 계층 구현

### 1.1 디렉토리 구조 생성

```bash
mkdir -p src/model
mkdir -p src/controller
mkdir -p src/view
touch src/model/__init__.py
touch src/controller/__init__.py
touch src/view/__init__.py
```

### 1.2 OperationStrategy 패턴 구현

**파일**: `src/model/operation_strategy.py`

```python
"""
연산 전략 패턴 구현

Strategy Pattern을 사용하여 각 연산을 독립적인 전략으로 분리합니다.
OCP 원칙을 준수하여 새로운 연산자 추가 시 기존 코드 수정 없이 확장 가능합니다.
"""

from abc import ABC, abstractmethod
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
        """지원하는 연산자 목록을 반환합니다."""
        return list(cls._strategies.keys())
```

**SOLID 원칙 적용**:
- ✅ **OCP**: 새로운 연산자 추가 시 Strategy 클래스만 추가하면 됨
- ✅ **SRP**: 각 Strategy는 하나의 연산만 담당
- ✅ **DIP**: Factory는 추상화(Protocol)에 의존

### 1.3 CalculatorModel 구현

**파일**: `src/model/calculator_model.py`

```python
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
        """첫 번째 숫자를 설정합니다."""
        self._first_number = value
        self._result = None
    
    def set_operator(self, operator: str) -> None:
        """연산자를 설정합니다."""
        if operator not in OperationStrategyFactory.get_supported_operators():
            raise ValueError(f"지원하지 않는 연산자입니다: {operator}")
        self._operator = operator
        self._result = None
    
    def set_second_number(self, value: float) -> None:
        """두 번째 숫자를 설정합니다."""
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
        """계산 준비가 되었는지 확인합니다."""
        return (
            self._first_number is not None
            and self._operator is not None
            and self._second_number is not None
        )
```

**SOLID 원칙 적용**:
- ✅ **SRP**: 계산 상태 관리와 계산 수행만 담당
- ✅ **DIP**: StrategyFactory를 통해 추상화에 의존

---

## Phase 2: 컨트롤러 계층 구현

### 2.1 InputValidator 구현

**파일**: `src/controller/input_validator.py`

```python
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
```

**SOLID 원칙 적용**:
- ✅ **SRP**: 입력 검증만 담당
- ✅ **ISP**: 필요한 메서드만 제공

### 2.2 ResultFormatter 구현

**파일**: `src/controller/result_formatter.py`

```python
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
```

**SOLID 원칙 적용**:
- ✅ **SRP**: 결과 포맷팅만 담당

### 2.3 CalculatorController 구현

**파일**: `src/controller/calculator_controller.py`

```python
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
            
            result_str = self.formatter.format_result(a, op, b, result)
            return True, result_str, None
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
```

**SOLID 원칙 적용**:
- ✅ **SRP**: View와 Model 간 중재만 담당
- ✅ **DIP**: Model에 의존하지만 구체 클래스가 아닌 인터페이스에 의존

---

## Phase 3: 뷰 계층 구현

### 3.1 DisplayWidget 구현

**파일**: `src/view/display_widget.py`

```python
"""
표시 위젯

계산 결과와 입력값을 표시하는 위젯입니다.
"""

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class DisplayWidget(QLineEdit):
    """계산기 표시 위젯"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setAlignment(Qt.AlignRight)
        self.setText("0")
        
        # 폰트 설정
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.setFont(font)
        
        # 스타일 설정
        self.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 10px;
            }
        """)
    
    def set_value(self, value: str) -> None:
        """표시할 값을 설정합니다."""
        self.setText(value)
```

### 3.2 NumberPad 구현

**파일**: `src/view/number_pad.py`

```python
"""
숫자 키패드 위젯

숫자 입력을 위한 버튼 그룹입니다.
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import pyqtSignal


class NumberPad(QWidget):
    """숫자 키패드 위젯"""
    
    # 시그널 정의
    number_clicked = pyqtSignal(str)  # 숫자 버튼 클릭
    sign_clicked = pyqtSignal()      # +/- 버튼 클릭
    dot_clicked = pyqtSignal()       # . 버튼 클릭
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """UI 초기화"""
        layout = QGridLayout()
        layout.setSpacing(5)
        
        # 숫자 버튼 배치 (7, 8, 9, 4, 5, 6, 1, 2, 3)
        numbers = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
        ]
        
        for num, row, col in numbers:
            btn = self._create_button(num)
            layout.addWidget(btn, row, col)
            btn.clicked.connect(lambda checked, n=num: self.number_clicked.emit(n))
        
        # 하단 버튼 (+/-, 0, .)
        sign_btn = self._create_button("+/-")
        zero_btn = self._create_button("0")
        dot_btn = self._create_button(".")
        
        layout.addWidget(sign_btn, 3, 0)
        layout.addWidget(zero_btn, 3, 1)
        layout.addWidget(dot_btn, 3, 2)
        
        sign_btn.clicked.connect(self.sign_clicked.emit)
        zero_btn.clicked.connect(lambda: self.number_clicked.emit("0"))
        dot_btn.clicked.connect(self.dot_clicked.emit)
        
        self.setLayout(layout)
    
    def _create_button(self, text: str) -> QPushButton:
        """버튼 생성"""
        btn = QPushButton(text)
        btn.setMinimumSize(60, 60)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        return btn
```

### 3.3 CalculatorWindow 구현

**파일**: `src/view/calculator_window.py`

```python
"""
계산기 메인 윈도우

PyQt5를 사용한 계산기 GUI 애플리케이션입니다.
"""

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


class CalculatorWindow(QMainWindow):
    """계산기 메인 윈도우"""
    
    def __init__(self):
        super().__init__()
        
        # 모델과 컨트롤러 초기화
        self.model = CalculatorModel()
        self.controller = CalculatorController(self.model)
        
        # 입력 상태 관리
        self._current_input = ""
        self._input_state = "first"  # "first", "operator", "second"
        
        self._init_ui()
        self._connect_signals()
    
    def _init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("계산기")
        self.setFixedSize(300, 400)
        
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
        """연산자 버튼 생성"""
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
    
    def _on_number_clicked(self, number: str):
        """숫자 버튼 클릭 처리"""
        if self._input_state == "first":
            self._current_input += number
            success, error = self.controller.set_first_number(self._current_input)
            if success:
                self.display.set_value(self._current_input)
            else:
                self._show_error(error)
        elif self._input_state == "second":
            self._current_input += number
            success, error = self.controller.set_second_number(self._current_input)
            if success:
                self.display.set_value(self._current_input)
            else:
                self._show_error(error)
    
    def _on_dot_clicked(self):
        """소수점 버튼 클릭 처리"""
        if '.' not in self._current_input:
            self._current_input += '.'
            if self._input_state == "first":
                self.display.set_value(self._current_input)
            elif self._input_state == "second":
                self.display.set_value(self._current_input)
    
    def _on_sign_clicked(self):
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
    
    def _on_operator_clicked(self, operator: str):
        """연산자 버튼 클릭 처리"""
        if self._input_state == "first":
            success, error = self.controller.set_operator(operator)
            if success:
                self._input_state = "operator"
                self._current_input = ""
            else:
                self._show_error(error)
        elif self._input_state == "operator":
            # 연산자 변경
            success, error = self.controller.set_operator(operator)
            if not success:
                self._show_error(error)
        elif self._input_state == "second":
            # 두 번째 숫자가 입력된 상태에서 연산자 클릭 시 계산 후 연산자 변경
            self._perform_calculation()
            success, error = self.controller.set_operator(operator)
            if success:
                self._input_state = "operator"
                self._current_input = ""
    
    def _on_calculate_clicked(self):
        """계산 버튼 클릭 처리"""
        self._perform_calculation()
    
    def _perform_calculation(self):
        """계산 수행"""
        if self.controller.model.is_ready_to_calculate():
            success, result, error = self.controller.calculate()
            if success:
                self.display.set_value(self.controller.get_display_value())
                # 결과를 첫 번째 숫자로 설정하여 연속 계산 가능
                self._input_state = "first"
                self._current_input = ""
            else:
                self._show_error(error)
        else:
            self._show_error("계산할 수 없습니다. 모든 값을 입력해주세요.")
    
    def _on_reset_clicked(self):
        """초기화 버튼 클릭 처리"""
        self.controller.reset()
        self._current_input = ""
        self._input_state = "first"
        self.display.set_value("0")
    
    def _show_error(self, message: str):
        """에러 메시지 표시"""
        QMessageBox.warning(self, "오류", message)
```

### 3.4 메인 진입점

**파일**: `src/gui_calculator.py` (새로 생성)

```python
"""
GUI 계산기 메인 진입점
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.view.calculator_window import CalculatorWindow


def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    
    window = CalculatorWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
```

---

## Phase 4: 테스트 작성

### 4.1 모델 테스트

**파일**: `tests/test_calculator_model.py`

```python
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
```

### 4.2 컨트롤러 테스트

**파일**: `tests/test_controller.py`

```python
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
```

---

## 실행 방법

### GUI 프로그램 실행

```bash
python src/gui_calculator.py
```

### 콘솔 프로그램 실행 (기존 유지)

```bash
python src/calculator.py
```

---

## 리팩토링 완료 체크리스트

### 코드 품질
- [ ] 모든 클래스가 단일 책임을 가짐
- [ ] Strategy 패턴으로 연산 확장 가능
- [ ] 의존성 역전 원칙 준수
- [ ] 타입 힌트 완비
- [ ] Docstring 완비

### 테스트
- [ ] 모델 테스트 작성 및 통과
- [ ] 컨트롤러 테스트 작성 및 통과
- [ ] 기존 arithmetic 테스트 통과
- [ ] 테스트 커버리지 80% 이상

### 기능
- [ ] 숫자 입력 동작
- [ ] 연산자 선택 동작
- [ ] 계산 수행 동작
- [ ] 에러 처리 동작
- [ ] 초기화 동작

### UI/UX
- [ ] 키패드 레이아웃 정상
- [ ] 표시 영역 정상
- [ ] 버튼 스타일 일관성
- [ ] 에러 메시지 표시

