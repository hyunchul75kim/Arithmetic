# 사칙연산 정확도 테스트 프로젝트

## 프로젝트 개요

이 프로젝트는 사칙연산(덧셈, 뺄셈, 곱셈, 나눗셈)의 정확도를 검증하는 테스트 프로젝트입니다. **RED-GREEN-REFACTOR** 방식의 TDD(Test-Driven Development) 방법론을 따라 개발됩니다.

## 테스트 정보

- **테스트 ID**: TC-CMM-001 (Common Module) / TC-AO-001 (Arithmetic Operations)
- **테스트 목적**: 사칙연산 정확도 테스트
- **테스트 범위**: 공통 모듈
- **작성일**: 2020-09-01
- **버전**: v1.0

## 테스트 환경

- **언어**: Python
- **IDE**: PyCharm
- **운영 체제**: Windows 10

## 테스트 케이스

### 기본 연산 테스트

| 테스트 케이스 | 입력값 | 예상값 | 중요도 | 상태 |
|------------|--------|--------|--------|------|
| 1 + 10 | 1, 10 | 11 | 중요 | 성공 |
| 0 + 1 | 0, 1 | 1 | 중요 | 성공 |
| 0 / 0 | 0, 0 | 예외 발생 (ArithmeticException) | 중요 | 성공 |
| -1 + (-10) | -1, -10 | -11 | 보통 | 성공 |
| 5 - 2 | 5, 2 | 3 | 중요 | 성공 |
| -5 * -3 | -5, -3 | 15 | 보통 | 성공 |
| 5 / 2 (정수 나눗셈) | 5, 2 | 2 | 중요 | 성공 |
| 5 ÷ 2 (몫 계산) | 5, 2 | 2.5 | 보통 | 성공 |
| 0 * 10 | 0, 10 | 0 | 낮음 | 성공 |
| -10 / 2 | -10, 2 | -5 | 중요 | 성공 |

### 예외 처리

- **0 / 0**: `ArithmeticException` 예외 발생 확인

## RED-GREEN-REFACTOR 방식

이 프로젝트는 TDD 방법론을 따릅니다:

1. **RED**: 실패하는 테스트 케이스를 먼저 작성 -- 개발 진행중
2. **GREEN**: 테스트를 통과하는 최소한의 코드 작성
3. **REFACTOR**: 코드를 개선하고 리팩토링

### 진행 단계

```
RED → GREEN → REFACTOR → RED → GREEN → REFACTOR → ...
```

## 프로젝트 구조

```
Arithmetic/
├── README.md
├── requirements.txt
├── src/
│   └── arithmetic.py      # 사칙연산 모듈
└── tests/
    └── test_arithmetic.py # 테스트 케이스
```

## 설치 및 실행

### 전제 조건

- Python 3.x 설치
- 모든 종속성이 올바르게 설치되어 있어야 함

### 설치

```bash
# 가상 환경 생성 (선택사항)
python -m venv venv

# 가상 환경 활성화
# Windows
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 테스트 실행

```bash
# pytest를 사용한 테스트 실행
pytest tests/

# 상세한 출력과 함께 실행
pytest tests/ -v

# 커버리지 리포트 생성
pytest tests/ --cov=src --cov-report=html
```

## 성공/실패 기준

- **성공**: 모든 테스트 사례가 예상한 결과를 생성
- **실패**: 테스트 케이스가 예상한 결과를 생성하지 않음

## 특별 절차

- 테스트 결과를 기록하고 테스트 사례 문서를 업데이트
- 모든 실패 사례는 즉시 개발팀에 전달

## 개발 진행 상황

- [x] RED: 테스트 케이스 작성 (완료)
- [ ] GREEN: 기본 기능 구현 (진행 예정)
- [ ] REFACTOR: 코드 개선
- [ ] 모든 테스트 케이스 통과 확인

## GREEN 단계 작업 목록

### 구현 우선순위

#### 높음 (High Priority) - 필수 구현 항목

1. **`add` 함수 구현**
   - [ ] 양수 덧셈: `add(1, 10) = 11`
   - [ ] 0 포함 덧셈: `add(0, 1) = 1`
   - [ ] 음수 덧셈: `add(-1, -10) = -11`
   - **테스트 케이스**: 3개 (`TestAddition` 클래스)

2. **`subtract` 함수 구현**
   - [ ] 기본 뺄셈: `subtract(5, 2) = 3`
   - **테스트 케이스**: 1개 (`TestSubtraction` 클래스)

3. **`multiply` 함수 구현**
   - [ ] 음수 곱셈: `multiply(-5, -3) = 15`
   - [ ] 0 곱셈: `multiply(0, 10) = 0`
   - **테스트 케이스**: 2개 (`TestMultiplication` 클래스)

4. **`divide` 함수 구현**
   - [ ] 정수 나눗셈: `divide(5, 2) = 2` (소수점 버림)
   - [ ] 음수 나눗셈: `divide(-10, 2) = -5`
   - [ ] 예외 처리: `divide(0, 0)` → `ZeroDivisionError` 발생
   - **테스트 케이스**: 3개 (`TestDivision` 클래스)

5. **`quotient` 함수 구현**
   - [ ] 소수점 몫: `quotient(5, 2) = 2.5`
   - **테스트 케이스**: 1개 (`TestQuotient` 클래스)

#### 중간 (Medium Priority) - 검증 항목

- [x] 예외 처리 구현 (`ZeroDivisionError`)
  - [x] `quotient` 함수 예외 처리 추가
  - [x] `quotient` 예외 처리 테스트 추가
  - [x] `divide` 추가 예외 케이스 검증 (양수/음수 ÷ 0)
- [x] 음수 처리 검증
  - [x] `subtract` 음수 조합 테스트 3개 추가
  - [x] `quotient` 음수 조합 테스트 3개 추가
  - [x] `add` 양수+음수 조합 테스트 추가
- [x] 경계값 처리 검증 (0 포함 연산)
  - [x] `subtract` 경계값 테스트 3개 추가
  - [x] `divide` 경계값 테스트 2개 추가
  - [x] `quotient` 경계값 테스트 2개 추가

#### 낮음 (Low Priority) - 개선 항목

- [x] 코드 최적화
  - [x] 타입 힌트 추가 (Python 3.10+ `|` 연산자 사용)
  - [x] 코드 가독성 향상
- [x] 추가 docstring 개선
  - [x] Google style docstring 적용
  - [x] 모든 함수에 매개변수, 반환값, 예외, 예제 추가
  - [x] 모듈 docstring 개선
- [x] 성능 최적화 (필요시)
  - [x] 타입 힌트로 IDE 지원 향상
  - [x] 코드 품질 향상 (기본 산술 연산은 이미 최적화됨)

### GREEN 단계 목표

- ✅ 총 **10개 테스트** 모두 통과
- ✅ 성공률 **100%**
- ✅ 코드 커버리지 **100%** (실제 로직 포함)
- ✅ 모든 예외 처리 검증 완료

### 검증 체크리스트

- [ ] `TestAddition` 클래스: 3개 테스트 통과
- [ ] `TestSubtraction` 클래스: 1개 테스트 통과
- [ ] `TestMultiplication` 클래스: 2개 테스트 통과
- [ ] `TestDivision` 클래스: 3개 테스트 통과
- [ ] `TestQuotient` 클래스: 1개 테스트 통과

## 라이선스

이 프로젝트는 테스트 목적으로 작성되었습니다.

