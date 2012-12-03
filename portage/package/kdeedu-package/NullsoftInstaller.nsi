; basic script template for NullsoftInstallerPackager
;
; Copyright 2010 Patrick Spendrin <ps_ml@gmx.de>
; adapted from marble.nsi

; registry stuff
!define regkey "Software\${company}\KDEEdu"
!define uninstkey "Software\Microsoft\Windows\CurrentVersion\Uninstall\KDEEdu"
 
!define startmenu "$SMPROGRAMS\KDEEdu"
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
!define MUI_ICON "${kdeedu-icon}"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_LICENSE "${kdeedu-root}\COPYING"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"
 

SetDateSave on
SetDatablockOptimize on
CRCCheck on
SilentInstall normal
 
InstallDir "$PROGRAMFILES\KDEEdu"
InstallDirRegKey HKLM "${regkey}" ""
 
;--------------------------------
 
AutoCloseWindow false
ShowInstDetails hide
 
 

Section "KDEEdu"
  ExecWait '"$INSTDIR\bin\kdeinit4.exe" "--shutdown"'
  WriteRegStr HKLM "${regkey}" "Install_Dir" "$INSTDIR"
  ; write uninstall strings
  WriteRegStr HKLM "${uninstkey}" "DisplayName" "KDE Edu (remove only)"
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
CreateShortCut "${startmenu}\Blinken.lnk" "$INSTDIR\bin\blinken.exe"
CreateShortCut "${startmenu}\Cantor.lnk" "$INSTDIR\bin\cantor.exe"
CreateShortCut "${startmenu}\KAlgebra.lnk" "$INSTDIR\bin\kalgebra.exe"
CreateShortCut "${startmenu}\Kalzium.lnk" "$INSTDIR\bin\kalzium.exe"
CreateShortCut "${startmenu}\Kanagram.lnk" "$INSTDIR\bin\kanagram.exe"
CreateShortCut "${startmenu}\KBruch.lnk" "$INSTDIR\bin\kbruch.exe"
CreateShortCut "${startmenu}\KGeography.lnk" "$INSTDIR\bin\kgeography.exe"
CreateShortCut "${startmenu}\KHangMan.lnk" "$INSTDIR\bin\khangman.exe"
CreateShortCut "${startmenu}\Kig.lnk" "$INSTDIR\bin\kig.exe"
CreateShortCut "${startmenu}\Kiten.lnk" "$INSTDIR\bin\kiten.exe"
CreateShortCut "${startmenu}\KLettres.lnk" "$INSTDIR\bin\klettres.exe"
CreateShortCut "${startmenu}\KMplot.lnk" "$INSTDIR\bin\kmplot.exe"
CreateShortCut "${startmenu}\KStars.lnk" "$INSTDIR\bin\kstars.exe"
CreateShortCut "${startmenu}\KTouch.lnk" "$INSTDIR\bin\ktouch.exe"
CreateShortCut "${startmenu}\KTurtle.lnk" "$INSTDIR\bin\kturtle.exe"
CreateShortCut "${startmenu}\KWordQuiz.lnk" "$INSTDIR\bin\kwordquiz.exe"
CreateShortCut "${startmenu}\Marble.lnk" "$INSTDIR\bin\marble.exe"
CreateShortCut "${startmenu}\Pairs.lnk" "$INSTDIR\bin\pairs.exe"
CreateShortCut "${startmenu}\Parley.lnk" "$INSTDIR\bin\parley.exe"
CreateShortCut "${startmenu}\Rocs.lnk" "$INSTDIR\bin\rocs.exe"
CreateShortCut "${startmenu}\Step.lnk" "$INSTDIR\bin\step.exe"
CreateShortCut "${startmenu}\Appearance Settings.lnk" "$INSTDIR\bin\kcmshell4.exe" "style" "$INSTDIR\bin\systemsettings.exe"
CreateShortCut "${startmenu}\Snorenotify.lnk" "$INSTDIR\bin\snorenotify.exe"
CreateShortCut "${startmenu}\Uninstall.lnk" $INSTDIR\uninstall.exe"
SectionEnd

;post install
Section
SetOutPath "$INSTDIR"
ExecWait '"$INSTDIR\bin\update-mime-database.exe" "$INSTDIR\share\mime"'
ExecWait '"$INSTDIR\bin\kbuildsycoca4.exe" "--noincremental"'
SectionEnd
 
; Uninstaller
; All section names prefixed by "Un" will be in the uninstaller
 
UninstallText "This will uninstall KDE Edu."
 
Section "Uninstall"
SetShellVarContext all
ExecWait '"$INSTDIR\bin\kdeinit4.exe" "--shutdown"'

DeleteRegKey HKLM "${uninstkey}"
DeleteRegKey HKLM "${regkey}"

Delete "${startmenu}\Uninstall.lnk"

RMDir /r "${startmenu}"
RMDir /r "$INSTDIR"

SectionEnd

