"""
GUI 계산기 메인 진입점

PyQt5를 사용한 계산기 GUI 애플리케이션의 진입점입니다.
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

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

