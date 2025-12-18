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
        """
        표시 위젯 초기화
        
        Args:
            parent: 부모 위젯
        """
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
        """
        표시할 값을 설정합니다.
        
        Args:
            value: 표시할 값 (문자열)
        """
        self.setText(value)
    
    def get_value(self) -> str:
        """
        현재 표시된 값을 반환합니다.
        
        Returns:
            현재 표시된 값
        """
        return self.text()

