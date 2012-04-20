; basic script template for 
;
; Copyright 2010 Patrick Spendrin <ps_ml@gmx.de>
; adapted from marble.nsi

; registry stuff
!define regkey "Software\${company}\Amarok"
!define uninstkey "Software\Microsoft\Windows\CurrentVersion\Uninstall\Amarok"
 
!define startmenu "$SMPROGRAMS\Amarok"
!define uninstaller "uninstall.exe"
 
 Var StartMenuFolder
 
 !define MUI_LANGDLL_ALLLANGUAGES
!define MUI_ICON "${amarok-icon}"
!define MUI_FINISHPAGE_RUN "$INSTDIR\bin\amarok.exe"
;save language
!define MUI_LANGDLL_REGISTRY_ROOT "HKLM" 
!define MUI_LANGDLL_REGISTRY_KEY "${regkey}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "Installer Language"

;Start Menu Folder Page Configuration
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKLM" 
!define MUI_STARTMENUPAGE_REGISTRY_KEY "${regkey}" 
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
;--------------------------------
 
XPStyle on
ShowInstDetails hide
ShowUninstDetails hide

SetCompressor /SOLID lzma


Name "${productname}"
Caption "${productname}"
 
OutFile "${setupname}"
 
!include "MUI2.nsh"


SetDateSave on
SetDatablockOptimize on
CRCCheck on
SilentInstall normal
 
InstallDir "$PROGRAMFILES\Amarok"
InstallDirRegKey HKLM "${regkey}" ""
 
;--------------------------------
 
AutoCloseWindow false
ShowInstDetails hide


!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "${amarok-root}\COPYING"
!insertmacro MUI_PAGE_DIRECTORY 
!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
; !insertmacro MUI_PAGE_FINISH


!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
; !insertmacro MUI_UNPAGE_FINISH
 
 

Section "Amarok"
  ExecWait '"$INSTDIR\bin\kdeinit4.exe" "--shutdown"'
  WriteRegStr HKLM "${regkey}" "Install_Dir" "$INSTDIR"
  ; write uninstall strings
 
  SetOutPath $INSTDIR
 
 
; package all files, recursively, preserving attributes
; assume files are in the correct places

File /a /r /x "*.nsi" /x "${setupname}" "${srcdir}\*.*" 

WriteUninstaller "${uninstaller}"
  
    ;Create shortcuts

!insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    SetShellVarContext all
    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Amarok.lnk" "$INSTDIR\bin\Amarok.exe"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Appearance Settings.lnk" "$INSTDIR\bin\kcmshell4.exe" "style" "$INSTDIR\bin\systemsettings.exe"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Snorenotify.lnk" "$INSTDIR\bin\snorenotify.exe"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\uninstall.exe"
      
!insertmacro MUI_STARTMENU_WRITE_END
SectionEnd


Section ;registry
  WriteRegStr HKLM "${uninstkey}" "DisplayName" "Amarok (remove only)"
  WriteRegStr HKLM "${uninstkey}" "UninstallString" '"$INSTDIR\${uninstaller}"'

SectionEnd



!macro AMAROK_ADD_LANGUAGE_PACKAGE LANG_SUFFIX
    SetOutPath "$INSTDIR"
    DetailPrint "Downloading: http://winkde.org/~pvonreth/downloads/l10n/${kde-version}/kde4-l10n-${LANG_SUFFIX}-${kde-version}.7z"
    NSISdl::download "http://winkde.org/~pvonreth/downloads/l10n/${kde-version}/kde4-l10n-${LANG_SUFFIX}-${kde-version}.7z" "$TEMP\kde4-l10n-${LANG_SUFFIX}-${kde-version}.7z"
	Nsis7z::Extract "$TEMP\kde4-l10n-${LANG_SUFFIX}-${kde-version}.7z" 
	Delete "$TEMP\kde4-l10n-${LANG_SUFFIX}-${kde-version}.7z"
!macroend

SubSection "Languages" SECTION_LANGAUAGES
Section /o "de" SECTION_LANGAUAGES_DE
    !insertmacro AMAROK_ADD_LANGUAGE_PACKAGE de
SectionEnd
Section /o "en_GB" SECTION_LANGAUAGES_EN_GB
    !insertmacro AMAROK_ADD_LANGUAGE_PACKAGE en_GB
SectionEnd
Section /o "it" SECTION_LANGAUAGES_IT
    !insertmacro AMAROK_ADD_LANGUAGE_PACKAGE it
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
 
 
Section "Uninstall"
SetShellVarContext all
ExecWait '"$INSTDIR\bin\kdeinit4.exe" "--shutdown"'

DeleteRegKey HKLM "${uninstkey}"
DeleteRegKey HKLM "${regkey}"

!insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder

RMDir /r "$SMPROGRAMS\$StartMenuFolder"
RMDir /r "$INSTDIR"

SectionEnd






!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SECTION_LANGAUAGES} $(DESC_SECTION_LANGAUAGES)
  !insertmacro MUI_DESCRIPTION_TEXT ${SECTION_LANGAUAGES_DE} $(DESC_SECTION_LANGAUAGES_DE)
  !insertmacro MUI_DESCRIPTION_TEXT ${SECTION_LANGAUAGES_EN_GB} $(DESC_SECTION_LANGAUAGES_EN_GB)
  !insertmacro MUI_DESCRIPTION_TEXT ${SECTION_LANGAUAGES_IT} $(DESC_SECTION_LANGAUAGES_IT)
!insertmacro MUI_FUNCTION_DESCRIPTION_END



  ;initialize the translations
!include "amarok_translation.nsh"


;installer Fcuntion
Function  .onInit 

  !insertmacro MUI_LANGDLL_DISPLAY

FunctionEnd

; Uninstaller Functions

Function un.onInit

  !insertmacro MUI_UNGETLANGUAGE
  
FunctionEnd

  
 



