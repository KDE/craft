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
Icon "${simon-root}\simon.ico"
;AddBrandingImage top 100

LicenseText "License page"
LicenseData "${simon-root}\LICENCE.txt"
 
SetDateSave on
SetDatablockOptimize on
CRCCheck on
SilentInstall normal
 
InstallDir "$PROGRAMFILES\Simon"
InstallDirRegKey HKLM "${regkey}" ""
 
Function .onInstSuccess
  SetOutPath "$INSTDIR"
  ExecWait '"$INSTDIR\bin\update-mime-database.exe" "$INSTDIR\share\mime"'
  ExecWait '"$INSTDIR\bin\kbuildsycoca4.exe" "--noincremental"'
FunctionEnd

; pages
; we keep it simple - leave out selectable installation types
; Page components
Page directory
Page license
Page instfiles
 
UninstPage uninstConfirm
UninstPage instfiles
 
;--------------------------------
 
AutoCloseWindow false
ShowInstDetails show
 
 
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
;FunctionEnd
