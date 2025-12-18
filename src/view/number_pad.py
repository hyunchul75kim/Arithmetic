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
        """
        숫자 키패드 초기화
        
        Args:
            parent: 부모 위젯
        """
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
        """
        버튼 생성
        
        Args:
            text: 버튼에 표시할 텍스트
            
        Returns:
            생성된 QPushButton 인스턴스
        """
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

