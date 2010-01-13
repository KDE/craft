echo %CD%
runas /profile /user:kde-devel "%comspec% /e:on /C %~d0 && cd %CD% && kdeenv.bat"