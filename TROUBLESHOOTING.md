# PyQt5 DLL 로드 실패 해결 방법

## 문제
```
ImportError: DLL load failed while importing QtWidgets: 지정된 모듈을 찾을 수 없습니다.
```

## 해결 방법

### 방법 1: PyQt5 재설치 (권장)

```bash
# PyQt5 완전 제거
pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip -y

# 캐시 정리
pip cache purge

# PyQt5 재설치
pip install PyQt5
```

### 방법 2: Visual C++ Redistributable 설치

Windows에서 PyQt5를 실행하려면 Visual C++ Redistributable이 필요합니다.

1. 다음 링크에서 다운로드:
   - [Visual C++ Redistributable for Visual Studio 2015-2022](https://aka.ms/vs/17/release/vc_redist.x64.exe)

2. 설치 후 재부팅 (필요한 경우)

### 방법 3: PyQt6로 전환 (대안)

PyQt5 대신 PyQt6를 사용할 수도 있습니다:

```bash
# PyQt5 제거
pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip -y

# PyQt6 설치
pip install PyQt6
```

그리고 코드를 수정:
- `from PyQt5.QtWidgets` → `from PyQt6.QtWidgets`
- `from PyQt5.QtCore` → `from PyQt6.QtCore`
- `from PyQt5.QtGui` → `from PyQt6.QtGui`

### 방법 4: 가상 환경에서 재설치

```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화 (Windows)
venv\Scripts\activate

# PyQt5 설치
pip install PyQt5
```

### 방법 5: 시스템 환경 변수 확인

PATH 환경 변수에 Python과 PyQt5 DLL 경로가 포함되어 있는지 확인:
- `C:\Python310\`
- `C:\Python310\Lib\site-packages\PyQt5\`

## 빠른 해결 스크립트

다음 스크립트를 실행하여 자동으로 재설치:

```bash
pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip -y
pip install --upgrade pip
pip install PyQt5
```

## 확인 방법

재설치 후 다음 명령으로 확인:

```python
python -c "from PyQt5.QtWidgets import QApplication; print('PyQt5 설치 성공!')"
```

