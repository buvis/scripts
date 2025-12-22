@echo off
chcp 1250 > NUL
call python %~dp0\%~n0 %*
