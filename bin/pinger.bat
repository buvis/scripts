@echo off
chcp 1250 > NUL
call pyenv exec python %~dp0\%~n0 %*
