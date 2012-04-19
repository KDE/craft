; basic script template for NullsoftInstallerPackager
;
; Copyright 2010 Patrick Spendrin <ps_ml@gmx.de>
; adapted from marble.nsi

; registry stuff
!define regkey "Software\${company}\Amarok"
!define uninstkey "Software\Microsoft\Windows\CurrentVersion\Uninstall\Amarok"
 
!define startmenu "$SMPROGRAMS\Amarok"
!define uninstaller "uninstall.exe"
 
;--------------------------------
 
XPStyle on
ShowInstDetails hide
ShowUninstDetails hide

SetCompressor /SOLID lzma


Name "${productname}"
Caption "${productname}"
 
OutFile "${setupname}"
 
!include "MUI2.nsh"
!define MUI_ICON "${amarok-icon}"
;Languages

  !insertmacro MUI_LANGUAGE "English" ;first language is the default language
  !insertmacro MUI_LANGUAGE "French"
  !insertmacro MUI_LANGUAGE "German"
  !insertmacro MUI_LANGUAGE "Spanish"
  !insertmacro MUI_LANGUAGE "SpanishInternational"
  !insertmacro MUI_LANGUAGE "SimpChinese"
  !insertmacro MUI_LANGUAGE "TradChinese"
  !insertmacro MUI_LANGUAGE "Japanese"
  !insertmacro MUI_LANGUAGE "Korean"
  !insertmacro MUI_LANGUAGE "Italian"
  !insertmacro MUI_LANGUAGE "Dutch"
  !insertmacro MUI_LANGUAGE "Danish"
  !insertmacro MUI_LANGUAGE "Swedish"
  !insertmacro MUI_LANGUAGE "Norwegian"
  !insertmacro MUI_LANGUAGE "NorwegianNynorsk"
  !insertmacro MUI_LANGUAGE "Finnish"
  !insertmacro MUI_LANGUAGE "Greek"
  !insertmacro MUI_LANGUAGE "Russian"
  !insertmacro MUI_LANGUAGE "Portuguese"
  !insertmacro MUI_LANGUAGE "PortugueseBR"
  !insertmacro MUI_LANGUAGE "Polish"
  !insertmacro MUI_LANGUAGE "Ukrainian"
  !insertmacro MUI_LANGUAGE "Czech"
  !insertmacro MUI_LANGUAGE "Slovak"
  !insertmacro MUI_LANGUAGE "Croatian"
  !insertmacro MUI_LANGUAGE "Bulgarian"
  !insertmacro MUI_LANGUAGE "Hungarian"
  !insertmacro MUI_LANGUAGE "Thai"
  !insertmacro MUI_LANGUAGE "Romanian"
  !insertmacro MUI_LANGUAGE "Latvian"
  !insertmacro MUI_LANGUAGE "Macedonian"
  !insertmacro MUI_LANGUAGE "Estonian"
  !insertmacro MUI_LANGUAGE "Turkish"
  !insertmacro MUI_LANGUAGE "Lithuanian"
  !insertmacro MUI_LANGUAGE "Slovenian"
  !insertmacro MUI_LANGUAGE "Serbian"
  !insertmacro MUI_LANGUAGE "SerbianLatin"
  !insertmacro MUI_LANGUAGE "Arabic"
  !insertmacro MUI_LANGUAGE "Farsi"
  !insertmacro MUI_LANGUAGE "Hebrew"
  !insertmacro MUI_LANGUAGE "Indonesian"
  !insertmacro MUI_LANGUAGE "Mongolian"
  !insertmacro MUI_LANGUAGE "Luxembourgish"
  !insertmacro MUI_LANGUAGE "Albanian"
  !insertmacro MUI_LANGUAGE "Breton"
  !insertmacro MUI_LANGUAGE "Belarusian"
  !insertmacro MUI_LANGUAGE "Icelandic"
  !insertmacro MUI_LANGUAGE "Malay"
  !insertmacro MUI_LANGUAGE "Bosnian"
  !insertmacro MUI_LANGUAGE "Kurdish"
  !insertmacro MUI_LANGUAGE "Irish"
  !insertmacro MUI_LANGUAGE "Uzbek"
  !insertmacro MUI_LANGUAGE "Galician"
  !insertmacro MUI_LANGUAGE "Afrikaans"
  !insertmacro MUI_LANGUAGE "Catalan"
  !insertmacro MUI_LANGUAGE "Esperanto"



SetDateSave on
SetDatablockOptimize on
CRCCheck on
SilentInstall normal
 
InstallDir "$PROGRAMFILES\Amarok"
InstallDirRegKey HKLM "${regkey}" ""
 
;--------------------------------
 
AutoCloseWindow false
ShowInstDetails hide
 
 

Section "Amarok"
  ExecWait '"$INSTDIR\bin\kdeinit4.exe" "--shutdown"'
  WriteRegStr HKLM "${regkey}" "Install_Dir" "$INSTDIR"
  ; write uninstall strings
  WriteRegStr HKLM "${uninstkey}" "DisplayName" "Amarok (remove only)"
  WriteRegStr HKLM "${uninstkey}" "UninstallString" '"$INSTDIR\${uninstaller}"'
 
  SetOutPath $INSTDIR
 
 
; package all files, recursively, preserving attributes
; assume files are in the correct places

File /a /r /x "*.nsi" /x "${setupname}" "${srcdir}\*.*" 

WriteUninstaller "${uninstaller}"
  
SectionEnd


; create shortcuts
Section "Shortcuts"
SetShellVarContext all
CreateDirectory "${startmenu}"
SetOutPath $INSTDIR ; for working directory
CreateShortCut "${startmenu}\Amarok.lnk" "$INSTDIR\bin\Amarok.exe"
CreateShortCut "${startmenu}\Appearance Settings.lnk" "$INSTDIR\bin\kcmshell4.exe" "style" "$INSTDIR\bin\systemsettings.exe"
CreateShortCut "${startmenu}\Snorenotify.lnk" "$INSTDIR\bin\snorenotify.exe"
CreateShortCut "${startmenu}\Uninstall.lnk" $INSTDIR\uninstall.exe"
SectionEnd

!macro ADD_LANGUAGE LANG_SUFFIX
    SetOutPath "$INSTDIR"
    DetailPrint "Downloading: http://winkde.org/~pvonreth/downloads/l10n/${kde-version}/kde4-l10n-${LANG_SUFFIX}-${kde-version}.7z"
    NSISdl::download "http://winkde.org/~pvonreth/downloads/l10n/${kde-version}/kde4-l10n-${LANG_SUFFIX}-${kde-version}.7z" "$TEMP\kde4-l10n-${LANG_SUFFIX}-${kde-version}.7z"
	Nsis7z::Extract "$TEMP\kde4-l10n-${LANG_SUFFIX}-${kde-version}.7z" 
	Delete "$TEMP\kde4-l10n-${LANG_SUFFIX}-${kde-version}.7z"
!macroend

SubSection "Languages" SECTION_LANGAUAGES
Section /o "de" SECTION_LANGAUAGES_DE
    !insertmacro ADD_LANGUAGE de
SectionEnd
Section /o "en_GB" SECTION_LANGAUAGES_EN_GB
    !insertmacro ADD_LANGUAGE en_GB
SectionEnd
SubSectionEnd



;post install
Section
SetOutPath "$INSTDIR"
ExecWait '"$INSTDIR\bin\update-mime-database.exe" "$INSTDIR\share\mime"'
ExecWait '"$INSTDIR\bin\kbuildsycoca4.exe" "--noincremental"'
SectionEnd
 
; Uninstaller
; All section names prefixed by "Un" will be in the uninstaller
 
UninstallText "This will uninstall Amarok."
 
Section "Uninstall"
SetShellVarContext all
ExecWait '"$INSTDIR\bin\kdeinit4.exe" "--shutdown"'

DeleteRegKey HKLM "${uninstkey}"
DeleteRegKey HKLM "${regkey}"

Delete "${startmenu}\Uninstall.lnk"

RMDir /r "${startmenu}"
RMDir /r "$INSTDIR"

SectionEnd

Function .onInit

  !insertmacro MUI_LANGDLL_DISPLAY

FunctionEnd

;initialize the translations
!include "amarok_translation.nsh"
 
 ;this must be called after the the strings are defined
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_LICENSE "${amarok-root}\COPYING"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

;this must be called after the strings and the pages are defined
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SECTION_LANGAUAGES} $(DESC_SECTION_LANGAUAGES)
  !insertmacro MUI_DESCRIPTION_TEXT ${SECTION_LANGAUAGES_DE} $(DESC_SECTION_LANGAUAGES_DE)
  !insertmacro MUI_DESCRIPTION_TEXT ${SECTION_LANGAUAGES_EN_GB} $(DESC_SECTION_LANGAUAGES_EN_GB)
!insertmacro MUI_FUNCTION_DESCRIPTION_END





 



