# 중간 우선순위 검증 항목 구현 시나리오

## 개요
- **목표**: GREEN 단계에서 구현된 기능들이 올바르게 동작하는지 추가 검증
- **범위**: 예외 처리, 음수 처리, 경계값 처리 검증
- **방법론**: 추가 테스트 케이스 작성 및 검증 스크립트 생성
- **원칙**: 최소 단위로 하나씩 검증 항목 추가

---

## 현재 상태 분석

### 이미 구현된 항목
1. ✅ **예외 처리 (`ZeroDivisionError`)**: `divide` 함수에 이미 구현됨
   - `test_divide_by_zero_exception` 테스트로 검증됨
   - 하지만 `quotient` 함수의 예외 처리는 없음

2. ✅ **음수 처리**: 일부 테스트 케이스 존재
   - `test_add_negative_numbers`: 음수 덧셈
   - `test_multiply_negative_numbers`: 음수 곱셈
   - `test_divide_negative_by_positive`: 음수 나눗셈
   - 하지만 `subtract`와 `quotient`의 음수 처리는 검증되지 않음

3. ✅ **경계값 처리 (0 포함 연산)**: 일부 테스트 케이스 존재
   - `test_add_0_and_1`: 0 포함 덧셈
   - `test_multiply_by_zero`: 0 곱셈
   - 하지만 `subtract`, `divide`, `quotient`의 0 처리 검증 부족

---

## 구현 전략

### 1. 검증 항목별 접근 방법
- **예외 처리**: `quotient` 함수에도 0으로 나누기 예외 처리 추가 및 테스트
- **음수 처리**: 각 함수별 음수 조합 테스트 케이스 추가
- **경계값 처리**: 0을 포함한 다양한 조합 테스트 케이스 추가

### 2. 구현 순서
1. 예외 처리 검증 강화 (`quotient` 함수)
2. 음수 처리 검증 강화 (각 함수별)
3. 경계값 처리 검증 강화 (0 포함 연산)

---

## 단계별 구현 시나리오

### Phase 1: 예외 처리 검증 강화

#### Step 1.1: `quotient` 함수 예외 처리 추가
- **현재 상태**: `quotient` 함수는 0으로 나누기 시 Python 기본 예외 발생
- **목표**: 명시적으로 `ZeroDivisionError` 처리
- **구현**: 
  ```python
  def quotient(a, b):
      """몫 계산 함수 (소수점 포함)"""
      if b == 0:
          raise ZeroDivisionError
      return a / b
  ```
- **검증**: 기존 테스트가 여전히 통과하는지 확인

#### Step 1.2: `quotient` 함수 예외 처리 테스트 추가
- **테스트 케이스**: `test_quotient_by_zero_exception`
- **구현**:
  ```python
  def test_quotient_by_zero_exception(self):
      """0으로 나누기 → ZeroDivisionError 예외 발생"""
      with pytest.raises(ZeroDivisionError):
          quotient(10, 0)
  ```
- **검증**: `pytest tests/test_arithmetic.py::TestQuotient::test_quotient_by_zero_exception -v`
- **예상 결과**: ✅ 통과

#### Step 1.3: `divide` 함수 추가 예외 케이스 검증
- **테스트 케이스**: `test_divide_positive_by_zero`, `test_divide_negative_by_zero`
- **목표**: 양수/음수를 0으로 나누는 경우 모두 검증
- **검증**: `pytest tests/test_arithmetic.py::TestDivision -v`
- **예상 결과**: 모든 테스트 통과

---

### Phase 2: 음수 처리 검증 강화

#### Step 2.1: `subtract` 함수 음수 처리 테스트 추가
- **테스트 케이스**: 
  - `test_subtract_negative_numbers`: 음수 - 음수
  - `test_subtract_positive_from_negative`: 음수 - 양수
  - `test_subtract_negative_from_positive`: 양수 - 음수
- **구현**:
  ```python
  def test_subtract_negative_numbers(self):
      """-5 - (-2) = -3"""
      assert subtract(-5, -2) == -3
  
  def test_subtract_positive_from_negative(self):
      """-10 - 5 = -15"""
      assert subtract(-10, 5) == -15
  
  def test_subtract_negative_from_positive(self):
      """10 - (-5) = 15"""
      assert subtract(10, -5) == 15
  ```
- **검증**: `pytest tests/test_arithmetic.py::TestSubtraction -v`
- **예상 결과**: 모든 테스트 통과

#### Step 2.2: `quotient` 함수 음수 처리 테스트 추가
- **테스트 케이스**:
  - `test_quotient_negative_by_positive`: 음수 ÷ 양수
  - `test_quotient_positive_by_negative`: 양수 ÷ 음수
  - `test_quotient_negative_by_negative`: 음수 ÷ 음수
- **구현**:
  ```python
  def test_quotient_negative_by_positive(self):
      """-10 ÷ 2 = -5.0"""
      assert quotient(-10, 2) == -5.0
  
  def test_quotient_positive_by_negative(self):
      """10 ÷ (-2) = -5.0"""
      assert quotient(10, -2) == -5.0
  
  def test_quotient_negative_by_negative(self):
      """-10 ÷ (-2) = 5.0"""
      assert quotient(-10, -2) == 5.0
  ```
- **검증**: `pytest tests/test_arithmetic.py::TestQuotient -v`
- **예상 결과**: 모든 테스트 통과

#### Step 2.3: `add` 함수 추가 음수 조합 테스트
- **테스트 케이스**: `test_add_positive_and_negative`
- **구현**:
  ```python
  def test_add_positive_and_negative(self):
      """10 + (-5) = 5"""
      assert add(10, -5) == 5
      assert add(-5, 10) == 5
  ```
- **검증**: `pytest tests/test_arithmetic.py::TestAddition -v`
- **예상 결과**: 모든 테스트 통과

---

### Phase 3: 경계값 처리 검증 강화

#### Step 3.1: `subtract` 함수 경계값 테스트 추가
- **테스트 케이스**:
  - `test_subtract_zero_from_positive`: 양수 - 0
  - `test_subtract_positive_from_zero`: 0 - 양수
  - `test_subtract_zero_from_zero`: 0 - 0
- **구현**:
  ```python
  def test_subtract_zero_from_positive(self):
      """10 - 0 = 10"""
      assert subtract(10, 0) == 10
  
  def test_subtract_positive_from_zero(self):
      """0 - 10 = -10"""
      assert subtract(0, 10) == -10
  
  def test_subtract_zero_from_zero(self):
      """0 - 0 = 0"""
      assert subtract(0, 0) == 0
  ```
- **검증**: `pytest tests/test_arithmetic.py::TestSubtraction -v`
- **예상 결과**: 모든 테스트 통과

#### Step 3.2: `divide` 함수 경계값 테스트 추가
- **테스트 케이스**:
  - `test_divide_zero_by_positive`: 0 ÷ 양수
  - `test_divide_positive_by_one`: 양수 ÷ 1
- **구현**:
  ```python
  def test_divide_zero_by_positive(self):
      """0 ÷ 5 = 0"""
      assert divide(0, 5) == 0
  
  def test_divide_positive_by_one(self):
      """10 ÷ 1 = 10"""
      assert divide(10, 1) == 10
  ```
- **검증**: `pytest tests/test_arithmetic.py::TestDivision -v`
- **예상 결과**: 모든 테스트 통과

#### Step 3.3: `quotient` 함수 경계값 테스트 추가
- **테스트 케이스**:
  - `test_quotient_zero_by_positive`: 0 ÷ 양수
  - `test_quotient_positive_by_one`: 양수 ÷ 1
- **구현**:
  ```python
  def test_quotient_zero_by_positive(self):
      """0 ÷ 5 = 0.0"""
      assert quotient(0, 5) == 0.0
  
  def test_quotient_positive_by_one(self):
      """10 ÷ 1 = 10.0"""
      assert quotient(10, 1) == 10.0
  ```
- **검증**: `pytest tests/test_arithmetic.py::TestQuotient -v`
- **예상 결과**: 모든 테스트 통과

---

## 최종 검증

### Step 4: 전체 테스트 실행
- **명령어**: `pytest tests/ -v`
- **예상 결과**: 
  - 기존 10개 테스트 + 새로 추가된 테스트 모두 통과
  - 성공률 100%

### Step 5: 커버리지 확인
- **명령어**: `pytest tests/ --cov=src --cov-report=term-missing`
- **예상 결과**: 
  - 코드 커버리지 100% 유지
  - 모든 예외 처리 경로 검증됨

### Step 6: 검증 리포트 생성
- **목적**: 추가된 검증 항목들을 문서화
- **내용**: 
  - 예외 처리 검증 결과
  - 음수 처리 검증 결과
  - 경계값 처리 검증 결과

---

## 예상 추가 테스트 케이스 요약

### 예외 처리 (1개 추가)
- `test_quotient_by_zero_exception`

### 음수 처리 (6개 추가)
- `test_subtract_negative_numbers`
- `test_subtract_positive_from_negative`
- `test_subtract_negative_from_positive`
- `test_quotient_negative_by_positive`
- `test_quotient_positive_by_negative`
- `test_quotient_negative_by_negative`
- `test_add_positive_and_negative`

### 경계값 처리 (7개 추가)
- `test_subtract_zero_from_positive`
- `test_subtract_positive_from_zero`
- `test_subtract_zero_from_zero`
- `test_divide_zero_by_positive`
- `test_divide_positive_by_one`
- `test_quotient_zero_by_positive`
- `test_quotient_positive_by_one`

**총 추가 예상 테스트**: 약 14개

---

## 검증 체크리스트

각 단계 완료 후 확인:

- [ ] Phase 1: 예외 처리 검증 강화
  - [ ] `quotient` 함수 예외 처리 추가
  - [ ] `quotient` 예외 처리 테스트 통과
  - [ ] `divide` 추가 예외 케이스 검증
- [ ] Phase 2: 음수 처리 검증 강화
  - [ ] `subtract` 음수 처리 테스트 통과
  - [ ] `quotient` 음수 처리 테스트 통과
  - [ ] `add` 추가 음수 조합 테스트 통과
- [ ] Phase 3: 경계값 처리 검증 강화
  - [ ] `subtract` 경계값 테스트 통과
  - [ ] `divide` 경계값 테스트 통과
  - [ ] `quotient` 경계값 테스트 통과
- [ ] 전체 테스트: 모든 테스트 통과
- [ ] 코드 커버리지: 100% 유지

---

## 주의사항

1. **기존 테스트 유지**: 기존 10개 테스트는 모두 통과해야 함
2. **최소 변경 원칙**: 기존 코드는 최소한으로만 수정
3. **점진적 추가**: 하나의 Phase씩 완료 후 다음으로 진행
4. **문서화**: 추가된 테스트 케이스는 README.md에 반영

---

## 작성일
- **시나리오 작성일**: 2025-12-16
- **예상 구현 완료일**: 승인 후 진행

