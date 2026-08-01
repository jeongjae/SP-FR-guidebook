@echo off
rem 가이드북 로컬 서버 실행 (PC·모바일 열람용)
cd /d "%~dp0"
set PORT=8000
if not "%1"=="" set PORT=%1

echo ==============================================
echo  TP 유럽 여행 가이드북 서버 시작
echo    PC에서:     http://localhost:%PORT%
echo    모바일에서: http://^<PC IP 주소^>:%PORT%  (같은 Wi-Fi)
echo    PC IP 확인: 아래 IPv4 주소 참조
ipconfig | findstr /i "IPv4"
echo    종료: Ctrl+C
echo ==============================================

python -m http.server %PORT% --directory site
