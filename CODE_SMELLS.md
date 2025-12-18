# 코드스멜 목록 (Code Smells)

이 문서는 현재 프로젝트에서 발견된 코드스멜과 리팩토링이 필요한 부분을 정리한 것입니다.

## 목차

1. [구조적 문제 (Structural Issues)](#구조적-문제)
2. [설계 문제 (Design Issues)](#설계-문제)
3. [코드 품질 문제 (Code Quality Issues)](#코드-품질-문제)
4. [의존성 문제 (Dependency Issues)](#의존성-문제)
5. [테스트 관련 문제 (Testing Issues)](#테스트-관련-문제)

---

## 구조적 문제 (Structural Issues)

### 1. Long Method (긴 메서드)

**위치**: `src/view/calculator_window.py`

**문제점**:
- `_init_ui()` 메서드가 75줄 이상으로 길고 여러 책임을 가짐
- UI 초기화, 버튼 생성, 스타일 설정, 시그널 연결이 모두 한 메서드에 집중

**영향도**: 중간

**리팩토링 제안**:
```python
# 분리 제안:
- _init_ui() → _setup_main_layout(), _setup_display(), _setup_number_pad(), _setup_operators(), _setup_actions()
```

**참고 파일**: `src/view/calculator_window.py:50-124`

---

### 2. Duplicated Code (중복 코드)

**위치**: `src/view/calculator_window.py`

**문제점**:
- `_on_number_clicked()` 메서드에서 "first"와 "second" 상태 처리 로직이 거의 동일
- 숫자 입력 검증 및 표시 로직이 중복됨

**영향도**: 높음

**리팩토링 제안**:
```python
# 공통 메서드 추출:
def _handle_number_input(self, number: str, state: str) -> None:
    """숫자 입력 처리 공통 로직"""
    if self._current_input == "0":
        self._current_input = number
    else:
        self._current_input += number
    
    if state == "first":
        success, error = self.controller.set_first_number(self._current_input)
    else:
        success, error = self.controller.set_second_number(self._current_input)
    
    if success:
        self.display.set_value(self._current_input)
    else:
        self._show_error(error or "올바른 숫자를 입력해주세요.")
```

**참고 파일**: `src/view/calculator_window.py:157-186`

---

### 3. Magic Strings (매직 문자열)

**위치**: `src/view/calculator_window.py`

**문제점**:
- 상태 관리에 문자열 리터럴 사용: `"first"`, `"operator"`, `"second"`
- 오타 위험 및 타입 안정성 부족

**영향도**: 중간

**리팩토링 제안**:
```python
# Enum 사용:
from enum import Enum

class InputState(Enum):
    FIRST = "first"
    OPERATOR = "operator"
    SECOND = "second"

# 사용:
self._input_state: InputState = InputState.FIRST
```

**참고 파일**: `src/view/calculator_window.py:45, 164, 176, 223, 230, 235, 254, 265`

---

### 4. Switch Statements (스위치 문)

**위치**: `src/calculator.py`

**문제점**:
- `calculate()` 함수에서 if-elif 체인으로 연산자 분기
- 새로운 연산자 추가 시 함수 수정 필요 (OCP 위반)

**영향도**: 중간

**리팩토링 제안**:
- 이미 `operation_strategy.py`에 Strategy 패턴이 구현되어 있으므로 활용
- `calculator.py`도 Strategy 패턴 사용하도록 리팩토링

**참고 파일**: `src/calculator.py:49-76`

---

## 설계 문제 (Design Issues)

### 5. Feature Envy (기능 질투)

**위치**: `src/view/calculator_window.py`

**문제점**:
- `_perform_calculation()` 메서드에서 `controller.model.is_ready_to_calculate()` 직접 호출
- View가 Model의 내부 상태를 직접 확인

**영향도**: 중간

**리팩토링 제안**:
```python
# Controller에 메서드 추가:
def is_ready_to_calculate(self) -> bool:
    """계산 준비 여부 확인"""
    return self.model.is_ready_to_calculate()

# View에서는:
if self.controller.is_ready_to_calculate():
    ...
```

**참고 파일**: `src/view/calculator_window.py:249`

---

### 6. Long Parameter List (긴 매개변수 목록)

**위치**: `src/controller/calculator_controller.py`

**문제점**:
- `calculate()` 메서드가 `tuple[bool, Optional[str], Optional[str]]` 반환
- 반환값이 복잡하고 가독성 저하

**영향도**: 낮음

**리팩토링 제안**:
```python
# Result 클래스 도입:
from dataclasses import dataclass

@dataclass
class CalculationResult:
    success: bool
    result: Optional[str] = None
    error: Optional[str] = None

def calculate(self) -> CalculationResult:
    ...
```

**참고 파일**: `src/controller/calculator_controller.py:80-103`

---

### 7. Data Clumps (데이터 덩어리)

**위치**: 여러 파일

**문제점**:
- `(bool, Optional[str])` 튜플이 여러 곳에서 반복 사용
- 의미가 명확하지 않음

**영향도**: 낮음

**리팩토링 제안**:
```python
# ValidationResult 클래스 도입:
@dataclass
class ValidationResult:
    is_valid: bool
    error: Optional[str] = None
```

**참고 파일**: 
- `src/controller/calculator_controller.py:28, 44, 64`
- `src/controller/input_validator.py:14, 38`

---

### 8. Primitive Obsession (원시 타입 집착)

**위치**: `src/view/calculator_window.py`

**문제점**:
- `_current_input`을 문자열로 관리
- 숫자 입력 상태를 문자열로 표현

**영향도**: 낮음

**리팩토링 제안**:
```python
# InputBuffer 클래스 도입:
class InputBuffer:
    def __init__(self):
        self._value: str = ""
    
    def append(self, char: str) -> None:
        ...
    
    def clear(self) -> None:
        ...
    
    def get_value(self) -> str:
        ...
```

**참고 파일**: `src/view/calculator_window.py:44`

---

## 코드 품질 문제 (Code Quality Issues)

### 9. Inline Style Sheets (인라인 스타일시트)

**위치**: `src/view/calculator_window.py`, `src/view/number_pad.py`, `src/view/display_widget.py`

**문제점**:
- CSS 스타일이 코드에 하드코딩됨
- 스타일 변경 시 코드 수정 필요
- 재사용성 저하

**영향도**: 낮음

**리팩토링 제안**:
```python
# 스타일 상수 분리:
class CalculatorStyles:
    OPERATOR_BUTTON = """
        QPushButton {
            background-color: #2196F3;
            color: white;
            font-size: 18px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #0b7dda;
        }
    """
```

**참고 파일**: 
- `src/view/calculator_window.py:91-116, 138-148`
- `src/view/number_pad.py:73-86`
- `src/view/display_widget.py:34-40`

---

### 10. Complex Conditional (복잡한 조건문)

**위치**: `src/view/calculator_window.py`

**문제점**:
- `_on_operator_clicked()` 메서드의 조건 분기가 복잡
- 상태 전이 로직이 명확하지 않음

**영향도**: 중간

**리팩토링 제안**:
```python
# 상태 패턴 또는 전략 패턴 적용:
class InputStateHandler:
    def handle_operator(self, operator: str) -> None:
        ...
```

**참고 파일**: `src/view/calculator_window.py:216-241`

---

### 11. Inconsistent Error Handling (일관성 없는 에러 처리)

**위치**: `src/view/calculator_window.py`

**문제점**:
- 일부 메서드는 에러를 무시하고, 일부는 표시
- 에러 메시지 형식이 일관되지 않음

**영향도**: 중간

**리팩토링 제안**:
- 모든 에러를 일관되게 처리하는 메커니즘 도입
- 에러 로깅 추가

**참고 파일**: `src/view/calculator_window.py:268-276`

---

### 12. Dead Code (죽은 코드)

**위치**: `src/arithmetic.py`

**문제점**:
- `if __name__ == "__main__"` 블록이 테스트/예제 코드 포함
- 프로덕션 코드에 불필요할 수 있음

**영향도**: 낮음

**리팩토링 제안**:
- 별도 예제 파일로 분리하거나 제거 검토

**참고 파일**: `src/arithmetic.py:137-179`

---

## 의존성 문제 (Dependency Issues)

### 13. System Path Manipulation (시스템 경로 조작)

**위치**: `src/gui_calculator.py`

**문제점**:
- `sys.path.insert(0, ...)` 사용
- 프로젝트 구조 변경 시 문제 발생 가능
- 패키지 설치 시 문제 가능

**영향도**: 높음

**리팩토링 제안**:
```python
# 상대 import 사용:
from src.view.calculator_window import CalculatorWindow

# 또는 setup.py로 패키지 설치
```

**참고 파일**: `src/gui_calculator.py:11-12`

---

### 14. Import 경로 불일치

**위치**: `src/calculator.py`

**문제점**:
- `from arithmetic import ...` (상대 경로 없음)
- 다른 파일들은 `from src.arithmetic import ...` 사용

**영향도**: 중간

**리팩토링 제안**:
```python
# 일관된 import:
from src.arithmetic import add, subtract, multiply, divide, quotient
```

**참고 파일**: `src/calculator.py:7`

---

### 15. Tight Coupling (강한 결합)

**위치**: `src/view/calculator_window.py`

**문제점**:
- View가 Model과 Controller를 모두 알고 있음
- Factory를 직접 import하여 사용

**영향도**: 낮음

**리팩토링 제안**:
- 의존성 주입을 통한 느슨한 결합 유지 (이미 부분적으로 구현됨)

**참고 파일**: `src/view/calculator_window.py:18, 37-41`

---

## 테스트 관련 문제 (Testing Issues)

### 16. Test Class Organization (테스트 클래스 구조)

**위치**: `tests/test_arithmetic.py`

**문제점**:
- 각 연산별로 별도 클래스 사용
- 일부 테스트 클래스는 메서드가 적음 (2개)

**영향도**: 낮음

**리팩토링 제안**:
- 통합하거나 더 세분화 (현재 구조도 나쁘지 않음)

**참고 파일**: `tests/test_arithmetic.py`

---

### 17. Missing Test Coverage (테스트 커버리지 부족)

**위치**: 전체 프로젝트

**문제점**:
- View 계층 테스트 없음
- 통합 테스트 부족
- 에지 케이스 테스트 부족

**영향도**: 중간

**리팩토링 제안**:
- GUI 테스트 추가 (QTest 사용)
- 통합 테스트 시나리오 추가

**참고 파일**: 전체 테스트 파일

---

## 우선순위별 정리

### 높은 우선순위 (High Priority)
1. **System Path Manipulation** (#13) - `src/gui_calculator.py`
2. **Duplicated Code** (#2) - `src/view/calculator_window.py`
3. **Import 경로 불일치** (#14) - `src/calculator.py`

### 중간 우선순위 (Medium Priority)
4. **Long Method** (#1) - `src/view/calculator_window.py`
5. **Magic Strings** (#3) - `src/view/calculator_window.py`
6. **Feature Envy** (#5) - `src/view/calculator_window.py`
7. **Complex Conditional** (#10) - `src/view/calculator_window.py`
8. **Inconsistent Error Handling** (#11) - `src/view/calculator_window.py`
9. **Missing Test Coverage** (#17) - 전체 프로젝트

### 낮은 우선순위 (Low Priority)
10. **Long Parameter List** (#6) - `src/controller/calculator_controller.py`
11. **Data Clumps** (#7) - 여러 파일
12. **Primitive Obsession** (#8) - `src/view/calculator_window.py`
13. **Inline Style Sheets** (#9) - View 파일들
14. **Dead Code** (#12) - `src/arithmetic.py`
15. **Tight Coupling** (#15) - `src/view/calculator_window.py`
16. **Test Class Organization** (#16) - `tests/test_arithmetic.py`

---

## 리팩토링 체크리스트

### Phase 1: 긴급 수정 (Critical)
- [ ] System Path Manipulation 수정 (#13)
- [ ] Import 경로 일관성 확보 (#14)
- [ ] 중복 코드 제거 (#2)

### Phase 2: 구조 개선 (Structural)
- [ ] Long Method 분리 (#1)
- [ ] Magic Strings를 Enum으로 변경 (#3)
- [ ] Feature Envy 해결 (#5)
- [ ] Complex Conditional 단순화 (#10)

### Phase 3: 품질 향상 (Quality)
- [ ] 에러 처리 일관성 확보 (#11)
- [ ] 테스트 커버리지 향상 (#17)
- [ ] 스타일 상수 분리 (#9)

### Phase 4: 세부 개선 (Polish)
- [ ] Long Parameter List 개선 (#6)
- [ ] Data Clumps 해결 (#7)
- [ ] Primitive Obsession 해결 (#8)
- [ ] Dead Code 정리 (#12)

---

## 참고 자료

- [Refactoring Catalog](https://refactoring.com/catalog/)
- [Code Smells](https://martinfowler.com/bliki/CodeSmell.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

---

**작성일**: 2024
**버전**: 1.0

