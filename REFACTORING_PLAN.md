# PyQt GUI 리팩토링 계획서

## 1단계: 현재 코드 분석 및 스멜 식별

### 1.1 코드 스멜 분석

#### `calculator.py`의 문제점

1. **God Object (신 객체)**
   - `main()` 함수가 너무 많은 책임을 가짐
   - 입력, 검증, 계산, 출력을 모두 처리

2. **Long Method (긴 메서드)**
   - `main()` 함수가 40줄 이상
   - 여러 관심사가 혼재

3. **Feature Envy (기능 질투)**
   - `calculate()` 함수가 연산자 문자열을 직접 비교
   - 연산 로직이 분산됨

4. **Switch Statements (스위치 문)**
   - `calculate()` 함수의 if-elif 체인
   - 새로운 연산자 추가 시 함수 수정 필요

5. **Duplicated Code (중복 코드)**
   - 입력 검증 로직이 반복됨
   - 에러 메시지 포맷팅이 중복

### 1.2 정적 분석 결과

#### 타입 안정성
- ✅ `arithmetic.py`: 타입 힌트가 잘 정의됨
- ⚠️ `calculator.py`: 일부 타입 힌트 부족

#### 순환 복잡도
- `calculate()` 함수: 복잡도 6 (높음)
- `main()` 함수: 복잡도 4 (중간)

#### 결합도
- `calculator.py`가 `arithmetic.py`에 직접 의존
- GUI로 전환 시 의존성 역전 필요

### 1.3 SOLID 원칙 위반 사항

#### SRP (Single Responsibility Principle) 위반
- `calculator.py`가 다음 책임을 모두 가짐:
  - 사용자 입력 처리
  - 입력 검증
  - 계산 수행
  - 결과 포맷팅
  - 에러 처리

#### OCP (Open/Closed Principle) 위반
- 새로운 연산자 추가 시 `calculate()` 함수 수정 필요
- 확장에는 열려있지 않음

#### DIP (Dependency Inversion Principle) 위반
- 구체적인 구현(`arithmetic` 모듈)에 직접 의존
- 추상화에 의존하지 않음

---

## 2단계: 아키텍처 설계

### 2.1 설계 패턴 선택

#### MVC (Model-View-Controller) 패턴 적용

```
┌─────────────────────────────────────────┐
│              View (PyQt GUI)           │
│  - CalculatorWindow (QMainWindow)       │
│  - NumberPad (QWidget)                  │
│  - Display (QLabel/QLineEdit)          │
│  - OperatorButtons (QPushButton)       │
└─────────────────┬─────────────────────┘
                   │
                   │ 사용자 입력
                   ▼
┌─────────────────────────────────────────┐
│         Controller                      │
│  - CalculatorController                 │
│  - InputValidator                       │
│  - ResultFormatter                      │
└─────────────────┬─────────────────────┘
                   │
                   │ 계산 요청
                   ▼
┌─────────────────────────────────────────┐
│         Model                           │
│  - CalculatorModel                      │
│  - OperationStrategy (Strategy Pattern) │
│  - ArithmeticOperations (기존)          │
└─────────────────────────────────────────┘
```

### 2.2 디렉토리 구조

```
Arithmetic/
├── src/
│   ├── __init__.py
│   ├── arithmetic.py          # 기존 (변경 없음)
│   ├── calculator.py          # 기존 (콘솔용, 유지)
│   ├── model/
│   │   ├── __init__.py
│   │   ├── calculator_model.py
│   │   └── operation_strategy.py
│   ├── controller/
│   │   ├── __init__.py
│   │   ├── calculator_controller.py
│   │   ├── input_validator.py
│   │   └── result_formatter.py
│   └── view/
│       ├── __init__.py
│       ├── calculator_window.py
│       ├── number_pad.py
│       └── display_widget.py
└── tests/
    ├── test_arithmetic.py     # 기존
    ├── test_calculator_model.py
    ├── test_controller.py
    └── test_view.py
```

---

## 3단계: SOLID 원칙 적용 설계

### 3.1 SRP (Single Responsibility Principle)

각 클래스는 단일 책임만 가짐:

- **CalculatorModel**: 계산 로직만 담당
- **CalculatorController**: 사용자 입력과 모델 간 중재
- **InputValidator**: 입력 검증만 담당
- **ResultFormatter**: 결과 포맷팅만 담당
- **CalculatorWindow**: UI 렌더링만 담당

### 3.2 OCP (Open/Closed Principle)

**Strategy Pattern** 적용:

```python
# operation_strategy.py
from abc import ABC, abstractmethod
from typing import Protocol

class OperationStrategy(Protocol):
    """연산 전략 인터페이스"""
    def execute(self, a: float, b: float) -> float:
        """연산을 수행합니다."""
        ...

class AddStrategy:
    def execute(self, a: float, b: float) -> float:
        from src.arithmetic import add
        return add(a, b)

class SubtractStrategy:
    def execute(self, a: float, b: float) -> float:
        from src.arithmetic import subtract
        return subtract(a, b)

# 새로운 연산자 추가 시 Strategy만 추가하면 됨
```

### 3.3 LSP (Liskov Substitution Principle)

모든 Strategy는 동일한 인터페이스를 구현하므로 서로 교체 가능

### 3.4 ISP (Interface Segregation Principle)

필요한 메서드만 포함하는 작은 인터페이스 사용

### 3.5 DIP (Dependency Inversion Principle)

```python
# Controller는 추상화에 의존
class CalculatorController:
    def __init__(self, model: CalculatorModel):
        self.model = model  # 구체 클래스가 아닌 인터페이스에 의존
```

---

## 4단계: 단계별 구현 계획

### Phase 1: 모델 계층 구현 (비즈니스 로직)

#### 1.1 OperationStrategy 패턴 구현
- [ ] `src/model/operation_strategy.py` 생성
- [ ] Strategy 인터페이스 정의
- [ ] 각 연산별 Strategy 클래스 구현
- [ ] Strategy Factory 구현

#### 1.2 CalculatorModel 구현
- [ ] `src/model/calculator_model.py` 생성
- [ ] 계산 상태 관리 (첫 번째 숫자, 연산자, 두 번째 숫자)
- [ ] Strategy를 사용한 계산 수행
- [ ] 예외 처리 (ZeroDivisionError 등)

**검증**: 단위 테스트 작성 및 통과

---

### Phase 2: 컨트롤러 계층 구현 (중재 로직)

#### 2.1 InputValidator 구현
- [ ] `src/controller/input_validator.py` 생성
- [ ] 숫자 입력 검증
- [ ] 연산자 입력 검증
- [ ] 에러 메시지 생성

#### 2.2 ResultFormatter 구현
- [ ] `src/controller/result_formatter.py` 생성
- [ ] 결과 포맷팅 로직
- [ ] 정수/소수점 처리

#### 2.3 CalculatorController 구현
- [ ] `src/controller/calculator_controller.py` 생성
- [ ] View와 Model 간 중재
- [ ] 입력 검증 위임
- [ ] 계산 요청 처리
- [ ] 결과 포맷팅 위임

**검증**: 단위 테스트 작성 및 통과

---

### Phase 3: 뷰 계층 구현 (UI)

#### 3.1 기본 위젯 구현
- [ ] `src/view/display_widget.py` 생성
  - 숫자 표시 영역
  - 입력 상태 표시
  
- [ ] `src/view/number_pad.py` 생성
  - 숫자 버튼 (0-9)
  - +/- 버튼
  - . 버튼

#### 3.2 연산자 버튼 구현
- [ ] 연산자 버튼 그룹 (+, -, *, /, //)
- [ ] 버튼 스타일링

#### 3.3 CalculatorWindow 구현
- [ ] `src/view/calculator_window.py` 생성
  - QMainWindow 상속
  - 레이아웃 구성
  - 위젯 배치
  - Controller 연결

**검증**: GUI 테스트 및 시각적 검증

---

### Phase 4: 통합 및 리팩토링

#### 4.1 의존성 주입 설정
- [ ] Controller에 Model 주입
- [ ] Window에 Controller 주입
- [ ] Factory 패턴으로 객체 생성

#### 4.2 에러 처리 개선
- [ ] 사용자 친화적 에러 메시지
- [ ] QMessageBox를 통한 에러 표시

#### 4.3 코드 정리
- [ ] 불필요한 코드 제거
- [ ] 타입 힌트 보완
- [ ] Docstring 추가

#### 4.4 테스트 작성
- [ ] 통합 테스트
- [ ] GUI 테스트 (선택사항)

---

## 5단계: 품질 검증

### 5.1 정적 분석
- [ ] pylint 실행 및 점수 확인
- [ ] mypy 타입 체크
- [ ] 코드 복잡도 측정

### 5.2 테스트 커버리지
- [ ] pytest-cov로 커버리지 확인
- [ ] 목표: 80% 이상

### 5.3 SOLID 원칙 검증
- [ ] 각 클래스의 책임 확인
- [ ] 의존성 방향 확인
- [ ] 확장성 검증

---

## 6단계: 문서화

### 6.1 코드 문서화
- [ ] 모든 클래스/메서드에 docstring 추가
- [ ] 타입 힌트 보완

### 6.2 사용자 가이드
- [ ] GUI 사용법 문서화
- [ ] README 업데이트

---

## 구현 우선순위

### 높음 (High Priority)
1. ✅ 모델 계층 (비즈니스 로직 분리)
2. ✅ Strategy 패턴 구현
3. ✅ 컨트롤러 계층

### 중간 (Medium Priority)
4. ✅ 기본 UI 구현
5. ✅ 입력 검증
6. ✅ 에러 처리

### 낮음 (Low Priority)
7. ✅ UI 스타일링
8. ✅ 추가 기능 (히스토리 등)
9. ✅ 성능 최적화

---

## 예상 이점

### 코드 품질
- ✅ 단일 책임 원칙 준수
- ✅ 테스트 가능성 향상
- ✅ 유지보수성 개선

### 확장성
- ✅ 새로운 연산자 추가 용이
- ✅ UI 변경 시 비즈니스 로직 영향 없음
- ✅ 다른 UI 프레임워크로 전환 가능

### 재사용성
- ✅ 모델 계층은 다른 프로젝트에서도 사용 가능
- ✅ Strategy 패턴으로 연산 로직 재사용

