@echo off
setlocal enabledelayedexpansion

rem 初始化导出目录
rd /S /Q export
mkdir export

rem 配置导出的版本, test.version
call :export_version test

goto :eof


rem export version
:export_version
echo process Version\%1.version
for /f "tokens=1,2" %%i in (Version\%1.version) do (
	if not "%%i"=="#" (
		set source=%%i
		set source=!source:/=\!
		set target=export\!source!

		rem 如果路径存在
		if exist !source! (
			rem 检查目标是文件夹还是文件
			for %%a in ("!source!") do set fileAttr=%%~ai
			if "!fileAttr:~0,1!"=="d" (
				rem 文件夹
				if not exist !target! (
					call :create_folder !target!
					xcopy !source! !target!\ /e
				)

			)else (
				rem 文件
				if not exist !target! (
					call :create_folder !target!
					echo !source!
					copy !source! !target!
				)
			)
		)else (
			rem 如果路径不存在
			echo not find !source!
		)
	)
)

goto :eof

:create_folder
if not exist %~p1 (
	mkdir %~p1
)