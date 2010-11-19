/* Copyright (C) 2010 Andre Heinecke <aheinecke@intevation.de>

   This library is free software; you can redistribute it and/or
   modify it under the terms of the GNU Library General Public
   License version 2 as published by the Free Software Foundation.

   This library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Library General Public License for more details.

   You should have received a copy of the GNU Library General Public License
   along with this library; see the file COPYING.LIB.  If not, write to
   the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.
*/
#include "gpglogger_wince.h"

#include <QtCore/QString>
#include <windows.h>

GPGLogger::GPGLogger() {
    gpgLoggingDriver = INVALID_HANDLE_VALUE;
    gpgLoggingDevice = INVALID_HANDLE_VALUE;

    bool ok = true;
    QString regValue = getWin32RegistryValue ( HKEY_LOCAL_MACHINE,
            QLatin1String("Drivers\\GnuPG_Log"),
            QLatin1String("enableLog"),
            &ok );
    if ( ! ok || regValue != "1" ) {
        OutputDebugStringW( (WCHAR*) QString::fromLatin1(
                    "GPGLogging: Regkey Drivers/GnuPG_Log not set.\n").utf16() );
    } else {
        // Activate the logging device
        gpgLoggingDevice = ActivateDevice (L"Drivers\\GnuPG_Log", 0);
        if ( gpgLoggingDevice == INVALID_HANDLE_VALUE) {
             OutputDebugStringW( (WCHAR*) QString::fromLatin1(
                        "GPGLogging: Device could not be activated.\n").utf16() );
        }
        // Try to open the gpgLoggingDriver
        gpgLoggingDriver = CreateFile (L"GPG2:", GENERIC_WRITE,
                FILE_SHARE_READ | FILE_SHARE_WRITE,
                NULL, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);

        if (gpgLoggingDriver == INVALID_HANDLE_VALUE) {
            OutputDebugStringW( (WCHAR*) QString::fromLatin1(
                        "GPGLogging: Driver not found.\n").utf16() );
        } else {
            DWORD nwritten;
            WCHAR * msg = (WCHAR*) QString::fromLatin1(
                    "GPGLogging: Driver loaded.\n").utf16();
            char * utfmsg = QString::fromWCharArray(msg).toUtf8().data();
            OutputDebugStringW( msg );
            WriteFile (gpgLoggingDriver, utfmsg, strlen(utfmsg), &nwritten, NULL);
        }
    }
}

GPGLogger::~GPGLogger()
{
    if ( gpgLoggingDriver != INVALID_HANDLE_VALUE ) {
        CloseHandle( gpgLoggingDriver );
    }
}

void GPGLogger::log ( const WCHAR* msg )
{
    if ( gpgLoggingDriver == INVALID_HANDLE_VALUE ) {
        return;
    } else
    {
        // Write to the driver
        DWORD nwritten; /* Contrary to the docs, required under WindowsCE.  */
        char * utfmsg =  QString::fromWCharArray(msg).toUtf8().data();
        if (!WriteFile (gpgLoggingDriver, utfmsg, strlen(utfmsg), &nwritten, NULL)) {
            OutputDebugStringW( (WCHAR*) QString::fromLatin1( "GPGLogging: Write failed.\n").utf16() );
        }
    }
}

QString GPGLogger::getWin32RegistryValue ( HKEY key, const QString& subKey, const QString& item, bool *ok )
{
#define FAILURE \
 { if (ok) \
  *ok = false; \
 return QString(); }

    if ( subKey.isEmpty() )
        FAILURE;
    HKEY hKey;
    TCHAR *lszValue;
    DWORD dwType=REG_SZ;
    DWORD dwSize;

    if ( ERROR_SUCCESS!=RegOpenKeyExW ( key,  (WCHAR*) subKey.utf16(), 0, KEY_READ, &hKey ) )
        FAILURE;

    if ( ERROR_SUCCESS!=RegQueryValueExW ( hKey, (WCHAR*) item.utf16(), NULL, NULL, NULL, &dwSize ) )
        FAILURE;

    lszValue = new TCHAR[dwSize];

    if ( ERROR_SUCCESS!=RegQueryValueExW ( hKey, (WCHAR*) item.utf16(), NULL, &dwType, ( LPBYTE ) lszValue, &dwSize ) ) {
        delete [] lszValue;
        FAILURE;
    }
    RegCloseKey ( hKey );

    QString res = QString::fromUtf16 ( ( const ushort* ) lszValue );
    delete [] lszValue;

    if (ok)
        *ok = true;

    return res;
}




