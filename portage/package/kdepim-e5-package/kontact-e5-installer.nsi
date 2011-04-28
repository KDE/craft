;kontact-e5-installer.nsi
;(c)2009-2011, Intevation GmbH
;Authors:
; Emanuel Schütze emanuel@intevation.de
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
;Includes

  ; Modern UI
  !include "MUI.nsh"

  ; Environment Variables
  !include "includes\EnvVarUpdate.nsh"

  ; Add (custom) plugin dir
  !addplugindir plugins

  ; String Replace function
  !include "includes\StrReplace.nsh"

  ; Windows Version detection
  !include "includes\getWinVer.nsi"

;--------------------------------
;Version Information (for installer file properties)

  VIProductVersion "${version_number}" ;needs integer format: x.x.x.x
  VIAddVersionKey "ProductName" "${productname_short}"
  VIAddVersionKey "Comments" "${productname_short} is Free Software"
  VIAddVersionKey "CompanyName" "${company}"
  VIAddVersionKey "LegalTrademarks" ""
  VIAddVersionKey "LegalCopyright" "${copyright}"
  VIAddVersionKey "FileDescription" "${description}"
  VIAddVersionKey "FileVersion" "${version_number} (build ${version_date})"


;--------------------------------
;General

  ; Define Name, File and Installdir of Installer
  Name "${productname}"
  OutFile "${setupname}"
  InstallDir "$PROGRAMFILES\${productname_short}"

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING

  ; MUI Settings / Header
  !define MUI_HEADERIMAGE

  !include "${branding}"

  ; Language Selection Dialog Settings to remember the installer language
  !define MUI_LANGDLL_REGISTRY_ROOT "HKLM"
  !define MUI_LANGDLL_REGISTRY_KEY "Software\${productname_short}" 
  !define MUI_LANGDLL_REGISTRY_VALUENAME "Installer Language"

  ; Custom Welcome Page

;--------------------------------
;Pages
  !define MUI_PAGE_CUSTOMFUNCTION_SHOW PrintNonAdminWarning
  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE ${license}
  !insertmacro MUI_PAGE_DIRECTORY
  Page custom CustomPageOptions
  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH

  !define MUI_PAGE_CUSTOMFUNCTION_SHOW un.PrintNonAdminWarning
  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH

;--------------------------------
;Supported Languages

  !insertmacro MUI_LANGUAGE "German"
  !insertmacro MUI_LANGUAGE "English"

;-------------------------------
;Reserve Files

  !insertmacro MUI_RESERVEFILE_LANGDLL
  !insertmacro MUI_RESERVEFILE_INSTALLOPTIONS
  ReserveFile "installer-options.ini"


;--------------------------------
;Installer Sections

Section ""
  SetOutPath "$INSTDIR"

  ; Store installation folder
  WriteRegStr HKLM "Software\${productname_short}" "" $INSTDIR

  ; Include the README file
  ;File "README-${version_date}.txt"

  ; Include the input files
  ; package all files, recursively, preserving attributes
  ; assume files are in the correct places

  File /a /r /x "*.nsi" /x "${setupname}" "${srcdir}\*"
   #!include "includes/inputfiles.nsh"

  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ; Create Registry keys
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${productname_short}" "DisplayName" "${productname_short} ${version_date}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${productname_short}" "Displayversion_number" "${version_number}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${productname_short}" "Displayversion_date" "${version_date}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${productname_short}" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${productname_short}" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${productname_short}" "NoRepair" 1

  ; Set Path to $PROFILE (default for ShortCut run in option -> default for Kowi file open dialog)
  SetOutPath "%HOMEDRIVE%%HOMEPATH%"

  # 'all users' shell folder is used (for $DESKTOP, $SMPROGRAMS, $QUICKLAUNCH,...)
  SetShellVarContext all

  # ** Start menu **
  # Delete old Start menu entries.
  RMDir /R  "$SMPROGRAMS\${productname_short} ${version_number}"
  # Check if the start menu entries where requested.
  !insertmacro MUI_INSTALLOPTIONS_READ $R0 "installer-options.ini" \
    "Field 2" "State"
  IntCmp $R0 0 no_start_menu
  # Create new Start menu entries
  CreateDirectory "$SMPROGRAMS\${productname}"
  CreateShortCut "$SMPROGRAMS\${productname}\${productname_short}.lnk" "$INSTDIR\bin\kontact.exe"
#  CreateShortCut "$SMPROGRAMS\${productname}\Akonadiconsole.lnk" "$INSTDIR\bin\akonadiconsole.exe"
  no_start_menu:

  # ** Desktop Icon **
  # Delete old Desktop link
  Delete "$DESKTOP\${productname_short}.lnk"
  # Check if the desktop entries where requested.
  !insertmacro MUI_INSTALLOPTIONS_READ $R0 "installer-options.ini" \
     "Field 3" "State"
  IntCmp $R0 0 no_desktop
  # Create new Desktop link
  CreateShortCut "$DESKTOP\${productname_short}.lnk" "$INSTDIR\bin\kontact.exe"
#  CreateShortCut "$DESKTOP\Akonadiconsole.lnk" "$INSTDIR\bin\akonadiconsole.exe"
  no_desktop:

  # ** Quick Launch **
  # Delete old Quick Launch Bar link
  Delete "$QUICKLAUNCH\${productname_short}.lnk"
  # Check if the quick launch bar entries where requested.
  !insertmacro MUI_INSTALLOPTIONS_READ $R0 "installer-options.ini" \
    "Field 4" "State"
  IntCmp $R0 0 no_quick_launch
  StrCmp $QUICKLAUNCH $TEMP no_quick_launch
  # Create new Quick Launch Bar link
  CreateShortCut "$QUICKLAUNCH\${productname_short}.lnk" "$INSTDIR\bin\kontact.exe"
  no_quick_launch:

  # ** Default Mail Application **
  # Check if the default mail apps entry was requested.
  !insertmacro MUI_INSTALLOPTIONS_READ $R0 "installer-options.ini" \
    "Field 5" "State"
  IntCmp $R0 0 no_default_apps
  # Create new Default Mail Apps Registry Entries
  WriteRegStr HKLM "Software\Clients\Mail\${productname_short}" "" "Kontact"
  WriteRegExpandStr HKLM "Software\Clients\Mail\${productname_short}" "LocalizedString" "@$INSTDIR\bin\ksendemail.exe"
  WriteRegStr HKLM "Software\Clients\Mail\${productname_short}\DefaultIcon" "" "$INSTDIR\bin\kontact.exe"
  WriteRegStr HKLM "Software\Clients\Mail\${productname_short}\Protocols\mailto" "" "URL:MailTo Protocol"
  WriteRegBin HKLM "Software\Clients\Mail\${productname_short}\Protocols\mailto" "EditFlags" "02000000"
  WriteRegStr HKLM "Software\Clients\Mail\${productname_short}\Protocols\mailto" "URL Protocol" ""
  WriteRegStr HKLM "Software\Clients\Mail\${productname_short}\Protocols\mailto\DefaultIcon" "" "$INSTDIR\bin\kontact.exe"
  WriteRegStr HKLM "Software\Clients\Mail\${productname_short}\Protocols\mailto\shell\open\command" "" "'$INSTDIR\bin\ksendemail.exe' %1"
  WriteRegStr HKLM "Software\Clients\Mail\${productname_short}\shell\open\command" "" "$INSTDIR\bin\kontact.exe"
  WriteRegStr HKLM "Software\Clients\Mail" "" "Kontact"  
  # Create File-Send-To link (for 'Default User')
  CreateShortCut "$PROFILE\..\Default User\SendTo\${productname_short}.lnk" "$INSTDIR\bin\ksendemail.exe" "--attach %1" "$INSTDIR\bin\kontact.exe"
  # Create File-Send-To link (for current user)
  CreateShortCut "$SENDTO\${productname_short}.lnk" "$INSTDIR\bin\ksendemail.exe" "--attach %1" "$INSTDIR\bin\kontact.exe"
  no_default_apps:


  ; Create killkde.bat 
  FileOpen $1 "$INSTDIR\bin\killkde.bat" "w"
  FileWrite $1 '@echo off $\r$\n'
  FileWrite $1 'kdeinit4 --terminate'
  FileClose $1

call CreateGlobals

  ; Create kwinstartmenurc (disabled kde start menu) 
  FileOpen $1 "$INSTDIR\share\config\kwinstartmenurc" "w"
  FileWrite $1 '[General] $\r$\n'
  FileWrite $1 'Enabled=false $\r$\n'
  FileClose $1

  ; Disable migrations
  FileOpen $1 "$INSTDIR\share\config\kmail-migratorrc" "w"
  FileWrite $1 "[Migration]$\r$\n"
  FileWrite $1 "Enabled=false$\r$\n"
  FileClose $1

  FileOpen $1 "$INSTDIR\share\config\kres-migratorrc" "w"
  FileWrite $1 "[Migration]$\r$\n"
  FileWrite $1 "Enabled=false$\r$\n"
  FileClose $1

  FileOpen $1 "$INSTDIR\share\config\kjotsmigratorrc" "w"
  FileWrite $1 "[Migration]$\r$\n"
  FileWrite $1 "Enabled=false$\r$\n"
  FileClose $1

  FileOpen $1 "$INSTDIR\share\config\kwalletrc" "w"
  FileWrite $1 "[Auto Allow]$\r$\n"
  FileWrite $1 "kdewallet=Akonadi Resource,Account Assistant,Kolab E5 RC,Kontact,Akonadi Agent$\r$\n"
  FileClose $1

  ; Set bin dir to PATH
  ; ${ENVVARUPDATE} $0 "PATH" "A" "HKLM" "$INSTDIR\bin"

  ; Set lib dir to PATH
  ; ${ENVVARUPDATE} $0 "PATH" "A" "HKLM" "$INSTDIR\lib"

  ; Set $INSTDIR to new environment variable KDEDIRS
  ; ${ENVVARUPDATE} $0 "KDEDIRS" "A" "HKLM" "$INSTDIR"

  ; Set $INSTDIR\share to new environment variable XDG_DATA_DIRS
  ; ${ENVVARUPDATE} $0 "XDG_DATA_DIRS" "A" "HKLM" "$INSTDIR\share;$INSTDIR"

  ; Set $INSTDIR\share\config to new environment variable XDG_CONFIG_DIRS
  ; ${ENVVARUPDATE} $0 "XDG_CONFIG_DIRS" "A" "HKLM" "$INSTDIR\share\config;$INSTDIR\xdg"

  ; Set $INSTDIR to new envrionment variable VIRTUOSO_HOME
  ; ${ENVVARUPDATE} $0 "VIRTUOSO_HOME" "A" "HKLM" "$INSTDIR"

  ;Register Virtuoso ODBC Driver
  ExecWait 'regsvr32.exe /s "$INSTDIR\lib\virtodbc.dll"'

  ; Createpost-install script
  FileOpen $1 "$TEMP\kde-post-install.bat" "w"
  FileWrite $1 'cd "$INSTDIR" $\r$\n'
  FileWrite $1 'set PATH="$INSTDIR\bin";%PATH% $\r$\n'
  FileWrite $1 'update-mime-database "$INSTDIR\share\mime" $\r$\n'
  FileWrite $1 'kbuildsycoca4 "--noincremental" $\r$\n'
  FileClose $1

  ;DetailPrint "Starte Post-Install-Skript"
  ExecDos::exec '"$SYSDIR\cmd.exe" /C "$TEMP\kde-post-install.bat"' "" "$INSTDIR\kde-post-install.log"
  Pop $R9 # return value

  ;If returned 0 then successful
  IntCmp $R9 0 success

  ; Looks like the removal failed so error out
  StrCpy $R8 "$(T_postInstallScriptFailed)" 
  StrCpy $R9 "$INSTDIR\kde-post-install.log"
  Call AbortDisplayLogOption

  success:
    Delete "$TEMP\kde-post-install.bat"
;    ReadRegStr $1 HKLM "Software\Microsoft\Windows\CurrentVersion\Run" \
;    "Akonaditray"
;    Exec $1 
    ; Return to caller
    Return

SectionEnd



;--------------------------------
;Install Functions
Function ".onInit"
  ; Language select dialog - not needed!
  !insertmacro MUI_LANGDLL_DISPLAY
  !insertmacro MUI_INSTALLOPTIONS_EXTRACT "installer-options.ini"
  call CheckExistingVersion
FunctionEnd

; Check whether application has already been installed.
Function CheckExistingVersion
  ClearErrors
  Push $0
  ReadRegStr $0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${productname_short}" "Displayversion_number"
  IfErrors leave 0
    MessageBox MB_YESNO|MB_ICONEXCLAMATION "${productname_short} $0 \
    $(T_AlreadyInstalled)" IDYES leave
    Abort
  leave:
FunctionEnd

Function CreateGlobals
; Create kdeglobals depending on the system
  push $R0
  call getWindowsVersion
  StrCmp $R0 '95' unsupportedVersion 0
  StrCmp $R0 '98' unsupportedVersion 0
  StrCmp $R0 'ME' unsupportedVersion 0
unsupportedVersion:
# TODO what to do here? abort? delete everything?
  StrCmp $R0 'Vista' modernGlobals 0
  StrCmp $R0 '7' modernGlobals 0
  !include "includes\xpglobals.nsi"
  Goto versionCheckDone

modernGlobals:
  !include "includes\modernglobals.nsi"

versionCheckDone:
  pop $0
FunctionEnd

# PrintNonAdminWarning

# Check whether the current user is in the Administrator group or an
# OS version without the need for an Administrator is in use. Print a
# diagnostic if this is not the case and abort installation.
Function PrintNonAdminWarning
  ClearErrors
  UserInfo::GetName
  IfErrors leave
  Pop $0
  UserInfo::GetAccountType
  Pop $1
  StrCmp $1 "Admin" leave +1
  MessageBox MB_OK|MB_ICONEXCLAMATION "$(T_AdminNeeded)"
  Quit
 leave:
FunctionEnd

; Custom Page for add Desktop, Startmenu and Quick Launch links
Function CustomPageOptions
  !insertmacro MUI_HEADER_TEXT "$(T_InstallOptions)" "$(T_InstallOptLinks)"

  # Note that the default selection is done in the ini file.
  !insertmacro MUI_INSTALLOPTIONS_WRITE "installer-options.ini" \
        "Field 1" "Text"  "$(T_InstOptLabelA)"
  !insertmacro MUI_INSTALLOPTIONS_WRITE "installer-options.ini" \
        "Field 2" "Text"  "$(T_InstOptFieldA)"
  !insertmacro MUI_INSTALLOPTIONS_WRITE "installer-options.ini" \
        "Field 3" "Text"  "$(T_InstOptFieldB)"
  !insertmacro MUI_INSTALLOPTIONS_WRITE "installer-options.ini" \
        "Field 4" "Text"  "$(T_InstOptFieldC)"
  !insertmacro MUI_INSTALLOPTIONS_WRITE "installer-options.ini" \
        "Field 5" "Text"  "$(T_InstOptFieldD)"
;  !insertmacro MUI_INSTALLOPTIONS_WRITE "installer-options.ini" \
;        "Field 6" "Text"  "$(T_InstOptFieldE)"

  !insertmacro MUI_INSTALLOPTIONS_DISPLAY "installer-options.ini"
FunctionEnd

; AbortDisplayLogOption - give the user the option to display an error log
; and abort the installation.
;       R8 - Error message
;       R9 - Log filename;
Function AbortDisplayLogOption

  ; Display a message box with the error 
  MessageBox MB_YESNO|MB_ICONSTOP "$R8$\r$\n$\r$\nMöchen Sie die Log-Datei '$R9' öffnen?" IDYES adlo_show_error_log

  ; If the user selects NO, simply abort the installation
  Abort "$R8" 
  Return

  adlo_show_error_log: 
    ;Otherwise show the error log first
    ExecShell "open" "$R9"
    Abort "$R8"  
    Return
FunctionEnd

;--------------------------------
;Uninstaller


Section "un."
  DetailPrint "Beende Prozesse"
  ExecDos::exec '"$SYSDIR\cmd.exe" /C "$INSTDIR\bin\killkde.bat"' ""
  
  ; Unregister Virtuoso
  ExecWait 'regsvr32.exe /u /s "$INSTDIR\lib\virtodbc.dll"'

  ; Delete installation dir
  RMDir /R "$INSTDIR"

  ; Delete configuration files
  ;RMDIR /R "$PROFILE\.config"
  
  ; Delete other kde files
  ;RMDIR /R "$PROFILE\.kde"
  ;RMDIR /R "$LOCALAPPDATA\.kde"

  ; Delete data files
  ;RMDIR /R "$PROFILE\.local"

  # 'all users' shell folder is used (for $DESKTOP, $SMPROGRAMS, $QUICKLAUNCH,...)
  SetShellVarContext all


  ; Delete start menu entries
  RMDir /R  "$SMPROGRAMS\${productname}"
  ; Delete Desktop Icon
  Delete "$DESKTOP\${productname_short}.lnk"
#  Delete "$DESKTOP\Akonadiconsole.lnk"
  ; Delete Quick Launch Link
  Delete "$QUICKLAUNCH\${productname_short}.lnk"
  
  ; Delete default mail client entry (Registry entries)
  DeleteRegKey HKLM "Software\Clients\Mail\${productname_short}" 
  ; Delete File-Send-To link (for 'Default User' and current user)
  Delete "$PROFILE\..\Default User\SendTo\${productname_short}.lnk" 
  Delete "$SENDTO\${productname_short}.lnk"
  ; Reset default mail client
  WriteRegStr HKLM "Software\Clients\Mail" "" ""


  ; Delete registry keys (if NO other installation exists)
  ReadRegStr $0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${productname_short}" "Displayversion_number"
  StrCmp $0 "${version_number}" 0 +3
      DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${productname_short}"
      DeleteRegKey /ifempty HKLM "Software\${productname_short}"

  ; Remove Akonaditray from autostart
;  DeleteRegValue HKLM "Software\Microsoft\Windows\CurrentVersion\Run" "Akonaditray"

  ; Remove bin dir from PATH
  ${un.ENVVARUPDATE} $0 "PATH" "R" "HKLM" "$INSTDIR\bin"

  ; Remove lib dir from PATH
  ${un.ENVVARUPDATE} $0 "PATH" "R" "HKLM" "$INSTDIR\lib"

  ; Remove bin dir from PATH
  ${un.ENVVARUPDATE} $0 "PATH" "R" "HKLM" "$INSTDIR\bin"

  ; Remove INSTDIr from KDEDIRS
  ${un.ENVVARUPDATE} $0 "KDEDIRS" "R" "HKLM" "$INSTDIR"

  ; Remove VIRTUOSO HOME
  ${un.ENVVARUPDATE} $0 "VIRTUOSO_HOME" "R" "HKLM" "$INSTDIR"

  ; Remove XDG_DATA_DIRS
  ${un.ENVVARUPDATE} $0 "XDG_DATA_DIRS" "R" "HKLM" "$INSTDIR\share;$INSTDIR"

  ; Remove XDG_CONFIG_DIRS
  ${un.ENVVARUPDATE} $0 "XDG_CONFIG_DIRS" "R" "HKLM" "$INSTDIR\share\config"

SectionEnd


;--------------------------------
;Uninstall Functions

Function un.onInit
  !insertmacro MUI_UNGETLANGUAGE
FunctionEnd

# PrintNonAdminWarning (uninstall)
Function un.PrintNonAdminWarning
  ClearErrors
  UserInfo::GetName
  IfErrors leave
  Pop $0
  UserInfo::GetAccountType
  Pop $1
  StrCmp $1 "Admin" leave +1
  MessageBox MB_OK|MB_ICONEXCLAMATION "$(T_AdminNeeded_uninstall)"
  Quit

 leave:
FunctionEnd








;---------------------------
; Language Strings
;---------------------------
# From Function CheckExistingVersion
LangString T_AlreadyInstalled ${LANG_ENGLISH} \
    "has already been installed.$\r$\nDo you want to\
    continue the installation of ${productname_short} ${version_date}?"
LangString T_AlreadyInstalled ${LANG_GERMAN} \
    "ist bereits auf ihrem System installiert.$\r$\nWollen Sie die \
    Installation von ${productname_short} ${version_date} fortsetzen?$\r$\n$\r$\nIhre \
    alte Installation wird dadurch überschrieben."

# From Custom Welcome Page
#
# Title
LangString T_WelcomeTitle ${LANG_ENGLISH} \
  "Welcome to the installation of  ${productname}"
LangString T_WelcomeTitle ${LANG_GERMAN} \
  "Willkommen bei der Installation von  ${productname}"
# description
LangString T_About ${LANG_ENGLISH} \
    "${description}, based upon KDE Kontact."
LangString T_About ${LANG_GERMAN} \
    "${description}, basierend auf KDE Kontact."
# version number
#LangString T_Aboutversion_number ${LANG_ENGLISH} \
#    "${productname_short} version: ${version_number}"
#LangString T_Aboutversion_number ${LANG_GERMAN} \
#    "${productname_short} Version: ${version_number}"
# version number
LangString T_Aboutversion_date ${LANG_ENGLISH} \
    "Release date: ${version_date}"
LangString T_Aboutversion_date ${LANG_GERMAN} \
    "Releasedatum: ${version_date}"



# From Function CustomPageOptions
# English
LangString T_InstallOptions ${LANG_ENGLISH} "Install Options"
LangString T_InstallOptLinks ${LANG_ENGLISH} "Start links"
LangString T_InstOptLabelA  ${LANG_ENGLISH} "Please select where ${productname_short} shall install links:"
LangString T_InstOptFieldA  ${LANG_ENGLISH} "Start Menu"
LangString T_InstOptFieldB  ${LANG_ENGLISH} "Desktop"
LangString T_InstOptFieldC  ${LANG_ENGLISH} "Quick Launch Bar"
LangString T_InstOptFieldD  ${LANG_ENGLISH} "Kontact as default mail client"
;LangString T_InstOptFieldE  ${LANG_ENGLISH} "Autostart Akonaditray"
#German
LangString T_InstallOptions ${LANG_GERMAN} "Installationsoptionen"
LangString T_InstallOptLinks ${LANG_GERMAN} "Startlinks"
LangString T_InstOptLabelA ${LANG_GERMAN} "Bitte wählen Sie, welche Verknüpfungen angelegt werden sollen:"
LangString T_InstOptFieldA ${LANG_GERMAN} "Startmenü"
LangString T_InstOptFieldB ${LANG_GERMAN} "Arbeitsfläche"
LangString T_InstOptFieldC ${LANG_GERMAN} "Schnellstartleiste"
LangString T_InstOptFieldD ${LANG_GERMAN} "Kontact als E-Mail-Standardprogramm"
;LangString T_InstOptFieldE ${LANG_GERMAN} "Akonadi in der Taskleiste anzeigen."

# From Function (un.)PrintNonAdminWarning
LangString T_AdminNeeded ${LANG_ENGLISH} \
   "Warning: Administrator permissions required for the installation of ${productname_short}."
LangString T_AdminNeeded ${LANG_GERMAN} \
   "Achtung: Für die Installation von ${productname_short} werden Administratorrechte benötigt."
LangString T_AdminNeeded_uninstall ${LANG_ENGLISH} \
   "Warning: Administrator permissions required for the uninstallation of ${productname_short}."
LangString T_AdminNeeded_uninstall ${LANG_GERMAN} \
   "Achtung: Für die Deinstallation von ${productname_short} werden Administratorrechte benötigt."


# kdeglobals - Contry Code
LangString T_kdeglobalsCountryCode ${LANG_ENGLISH} "en"
LangString T_kdeglobalsCountryCode ${LANG_GERMAN} "de"

# kdeglobal
LangString T_kdeglobalsLanguageCode ${LANG_ENGLISH} "en_us"
LangString T_kdeglobalsLanguageCode ${LANG_GERMAN} "de"

# post install script failed
LangString T_postInstallScriptfailed ${LANG_ENGLISH} "Post install script failed."
LangString T_postInstallScriptfailed ${LANG_GERMAN} "Post-Install-Skript fehlgeschlagen."

!include ${branding_locale}
