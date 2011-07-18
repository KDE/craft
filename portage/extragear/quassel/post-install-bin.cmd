@echo off

IF EXIST %APPDATA%\quassel-irc.org\quasselCert.pem  GOTO END
echo Generating a openssl certificate for Quassel

set  OPENSSL_CONF=%KDEROOT%\ssl\openssl.cnf
openssl req -x509 -nodes -days 365 -newkey rsa:1024 -subj "/C=DE/ST=None/L=None/O=None/CN=www.windows.kde.org"  -keyout %APPDATA%\quassel-irc.org\quasselCert.pem -out %APPDATA%\quassel-irc.org\quasselCert.pem

:END