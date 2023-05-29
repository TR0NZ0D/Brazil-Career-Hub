@echo off
setlocal EnableDelayedExpansion
set pathlist=
for /d %%D in (*) do (
    if %%~D neq venv (
       set pathlist=!pathlist! .\%%~D\
    )
)
echo Enabling virtual environment...
call .\venv\Scripts\activate
echo Checking project...
python .\manage.py check
echo Testing project...
python .\manage.py test
echo:
echo Validating project with pylint...
pylint --rcfile .pylintrc !pathlist!
echo:
echo Back-end validation finished
exit 0