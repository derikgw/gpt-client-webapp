@echo off
FOR /F "tokens=5 delims= " %%P IN ('netstat -ano ^| findstr /R /C:":5000 " ^| findstr /R /C:"LISTENING"') DO (
    SET "ProcessId=%%P"
    IF NOT "%%P"=="" (
        echo Found process listening on port 5000 with PID %%P. Killing process...
        taskkill /PID %%P /F
    ) ELSE (
        echo No process found listening on port 5000.
    )
)
echo Done.
