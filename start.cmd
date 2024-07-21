@echo off
cls

REM Define paths to your Python scripts
set TIMER_SCRIPT=startStopwatch.py
set CLOCK_SCRIPT=startClock.py

goto menu


REM Function to start the Stopwatch
:start_stopwatch
echo Starting Stopwatch...
start /B python3 %TIMER_SCRIPT%
goto :eof

REM Function to start the clock
:start_clock
echo Starting Clock...
start /B python3 %CLOCK_SCRIPT%
goto :eof

REM Function to start both Stopwatch and clock
:start_both
echo Starting Stopwatch and Clock...
call :start_stopwatch
call :start_clock
goto :eof

REM Display the menu
:menu
echo Please select an option:
echo 1) Start Stopwatch
echo 2) Start Clock
echo 3) Start Stopwatch and Clock
echo 4) Exit
set /p choice="Enter your choice: "

REM Handle the user's choice
if "%choice%"=="1" (
    cls
    call :start_stopwatch
) else if "%choice%"=="2" (
    cls
    call :start_clock
) else if "%choice%"=="3" (
    cls
    call :start_both
) else if "%choice%"=="4" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid option. Please try again.
    goto menu
)
pause