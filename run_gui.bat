@echo off
REM GUI 계산기 실행 스크립트

REM 프로젝트 루트에서 실행
cd /d %~dp0
python -m src.gui_calculator

