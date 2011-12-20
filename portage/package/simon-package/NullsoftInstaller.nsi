; basic script template for NullsoftInstallerPackager
;
;modified for simon by
; Copyright 2011 Patrick von Reth <patrick.vonreth@gmail.com>
; Copyright 2010 Patrick Spendrin <ps_ml@gmx.de>
; adapted from marble.nsi

; registry stuff

!define regkey "Software\${company}\Simon"
!define uninstkey "Software\Microsoft\Windows\CurrentVersion\Uninstall\Simon"
 
!define startmenu "$SMPROGRAMS\Simon"
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
!define MUI_ICON "${simon-root}\simon.ico"

!define MUI_HEADERIMAGE
    !define MUI_HEADERIMAGE_BITMAP "${simon-root}\installbanner.bmp"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_LICENSE "${simon-root}\LICENCE.txt"
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"
 


 
SetDateSave on
SetDatablockOptimize on
CRCCheck on
SilentInstall normal
 
InstallDir "$PROGRAMFILES\Simon"
InstallDirRegKey HKLM "${regkey}" ""
 
;--------------------------------
 
AutoCloseWindow false
ShowInstDetails hide
 
 
; beginning (invisible) section
Section
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
Section
SetShellVarContext all
CreateDirectory "${startmenu}"
SetOutPath $INSTDIR ; for working directory
CreateShortCut "${startmenu}\Simon.lnk" "$INSTDIR\bin\Simon.exe"
CreateShortCut "${startmenu}\simon.lnk" "$INSTDIR\bin\simon.exe" 
CreateShortCut "${startmenu}\simond.lnk" "$INSTDIR\bin\simond.exe"
CreateShortCut "${startmenu}\ksimond.lnk" "$INSTDIR\bin\ksimond.exe"
      
CreateShortCut "${startmenu}\sam.lnk" "$INSTDIR\bin\sam.exe" 
CreateShortCut "${startmenu}\ssc.lnk" "$INSTDIR\bin\ssc.exe" 
CreateShortCut "${startmenu}\sscd.lnk" "$INSTDIR\bin\sscd.exe" 
CreateShortCut "${startmenu}\afaras.lnk" "$INSTDIR\bin\afaras.exe"

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
 
UninstallText "This will uninstall Simon."
 
Section "Uninstall"
SetShellVarContext all
ExecWait '"$INSTDIR\bin\kdeinit4.exe" "--shutdown"'

DeleteRegKey HKLM "${uninstkey}"
DeleteRegKey HKLM "${regkey}"

Delete "${startmenu}\Uninstall.lnk"

RMDir /r "${startmenu}"
RMDir /r "$INSTDIR"

SectionEnd

;Function .onGUIInit
;  SetBrandingImage /RESIZETOFIT "${simon-root}\installbanner2.bmp"
;SetCtlColors $R0 FFFFFF FF0000
;FunctionEnd
