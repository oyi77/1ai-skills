@echo off
REM Gemini Image Generator - Quick Launcher
cd /d "%~dp0"

echo ========================================
echo Gemini Image Generator
echo ========================================
echo.

if "%1"=="" goto menu
if "%1"=="fashion" goto fashion
if "%1"=="electronics" goto electronics
if "%1"=="food" goto food
if "%1"=="beauty" goto beauty
if "%1"=="home" goto home
if "%1"=="batch" goto batch

goto menu

:menu
echo Choose category:
echo 1. Fashion
echo 2. Electronics
echo 3. Food
echo 4. Beauty
echo 5. Home
echo 6. Batch Process
echo.
set /p choice="Enter choice (1-6): "

if "%choice%"=="1" goto fashion_input
if "%choice%"=="2" goto electronics_input
if "%choice%"=="3" goto food_input
if "%choice%"=="4" goto beauty_input
if "%choice%"=="5" goto home_input
if "%choice%"=="6" goto batch
goto menu

:fashion_input
set /p product="Enter product name: "
python prompt_optimizer.py --category fashion --product "%product%"
pause
goto end

:electronics_input
set /p product="Enter product name: "
python prompt_optimizer.py --category electronics --product "%product%"
pause
goto end

:food_input
set /p product="Enter product name: "
python prompt_optimizer.py --category food --product "%product%"
pause
goto end

:beauty_input
set /p product="Enter product name: "
python prompt_optimizer.py --category beauty --product "%product%"
pause
goto end

:home_input
set /p product="Enter product name: "
python prompt_optimizer.py --category home --product "%product%"
pause
goto end

:fashion
python prompt_optimizer.py --category fashion --product %2
pause
goto end

:electronics
python prompt_optimizer.py --category electronics --product %2
pause
goto end

:food
python prompt_optimizer.py --category food --product %2
pause
goto end

:beauty
python prompt_optimizer.py --category beauty --product %2
pause
goto end

:home
python prompt_optimizer.py --category home --product %2
pause
goto end

:batch
echo.
echo Batch processing all images in input folder...
python workflow_runner.py --batch
pause
goto end

:end
