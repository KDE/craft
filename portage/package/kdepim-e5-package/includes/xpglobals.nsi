; xpglobals.nsi
;(c)2009-2011, Intevation GmbH
;Authors:
; Andre Heinecke aheinecke@intevation.de
;
; This program is free software; you can redistribute it and/or modify
; it under the terms of the GNU General Public License version 2,
; or, at your option, any later version as published by the Free
; Software Foundation
;
; This program is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.
;
; You should have received a copy of the GNU General Public License
; along with this program; if not, write to the Free Software
; Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
;
;--------------------------------
; This script writes a kdeglobalsrc as the default configuration for the
; Package

    FileOpen $1 "$INSTDIR\share\config\kdeglobals" "w"
    FileWrite $1 '[Locale] $\r$\n'
    FileWrite $1 'Country=$(T_kdeglobalsCountryCode) $\r$\n'
    FileWrite $1 'Language=$(T_kdeglobalsLanguageCode) $\r$\n'
    FileWrite $1 ' $\r$\n'
    FileWrite $1 '[General] $\r$\n'
    FileWrite $1 'font=Tahoma  $\r$\n'
    FileWrite $1 'menuFont=Tahoma $\r$\n'

    FileClose $1
