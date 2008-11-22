@echo off

call :sed [replace_this] %CD:\=/% %CD%\share\apps\cmake\modules\KDELibsDependenciesInternal.cmake
goto :eof


:per_line_replace
    ::
    set _string=%*
    
    call set _string=%%_string:%_orgstring%=%_replacestring%%%

    :: unquote the string
    set _string=###%_string%###
    set _string=%_string:"###=%
    set _string=%_string:###"=%
    set _string=%_string:###=%
    echo %_string%

    goto :eof

:sed
    :: this target will work like sed -e -i "s/%1/%2/g" %3
    :: one known problem besides being obviously brain damaged
    :: is that it eats all empty lines
    :: I'd call this a minor issue though
    set _orgstring=%1
    set _replacestring=%2
    set _filename=%3

    if exist %_filename%.tmp del %_filename%.tmp

    :: please keep in mind that we need the quotes to preserve the spaces at the start and
    :: end of the lines
    if not exist %_filename%.template (
        goto :eof
    )
    for /F "usebackq tokens=* delims=^;" %%G in (`type %_filename%.template`) do (
        call :per_line_replace "%%G" >> %_filename%.tmp )

    xcopy /Y %_filename%.tmp %_filename%

    del %_filename%.tmp