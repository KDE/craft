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

#ifndef GPGLOGGER_WINCE_H
#define GPGLOGGER_WINCE_H
#ifdef _WIN32_WCE
/**
 * @short Windows CE specific logging code
 * @author Andre Heinecke <aheinecke@intevation.de>
 *
 * Since there are few debug facilities availabe on Windows CE we use
 * a special gpg debug driver if it is availabe and the registry key
 * HKLM\Software\kde\useloggingdriver is set to true
 */
#include <windows.h>
class GPGLogger
{
    private:
        HANDLE gpgLoggingDriver;
        HANDLE gpgLoggingDevice;
    public:
        QString GPGLogger::getWin32RegistryValue ( HKEY key,
                const QString& subKey,
                const QString& item,
                bool *ok );
        GPGLogger();
        ~GPGLogger();
        void log( const WCHAR * msg);
};
#endif // _WIN32_WCE
#endif // GPGLOGGER_WINCE_H

