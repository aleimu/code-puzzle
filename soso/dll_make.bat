@echo off

REM 设置源文件的目录
set filepath=%1
REM 设置def文件的目录
set defpath=%~dp1%~n1.def
REM 设置生成的目标dll的路径
set dllpath=%~dp1%~n1.dll
set libpath=%~dp1%~n1.lib

IF NOT EXIST "%filepath%" (
	goto err
) ELSE (
	goto make
)

:err
echo 文件不存在！
set/p exepath=请拖拽文件这里或输入文件路径然后按下回车
IF NOT EXIST "%filepath%" (
	goto err
) ELSE (
	goto make
)

:make
echo 编译 %~nx1 -^> %~n1.dll
echo 正在编译 %~nx1 -^> %~n1.a
call go build -buildmode=c-archive %filepath%
echo 生成%~n1.a和%~n1.h文件

echo 正在编译 %~nx1.a -^> %~n1.dll
call gcc %defpath% %~dp1%~n1.a -shared -lwinmm -lWs2_32 -o %dllpath% -Wl,--out-implib,%libpath%
echo 生成%~n1.dll和%~n1.lib文件

REM 清除中间文件
for /r %%f in (*.a,*.o) do del %%f
echo 编译完成!
:end