; basic script template for NullsoftInstallerPackager
;
; Copyright 2010 Patrick Spendrin <ps_ml@gmx.de>
; adapted from marble.nsi

; registry stuff
!define regkey "Software\${company}\${productname}"
!define uninstkey "Software\Microsoft\Windows\CurrentVersion\Uninstall\${productname}"
 
!define startmenu "$SMPROGRAMS\${productname}"
!define uninstaller "uninstall.exe"
 
;--------------------------------
 
XPStyle on
ShowInstDetails hide
ShowUninstDetails hide
 
Name "${productname}"
Caption "${productname}"
 
OutFile "${setupname}"
 
SetDateSave on
SetDatablockOptimize on
CRCCheck on
SilentInstall normal
 
InstallDir "$PROGRAMFILES\${productname}"
InstallDirRegKey HKLM "${regkey}" ""
 
; pages
; we keep it simple - leave out selectable installation types
; Page components
Page directory
Page instfiles
 
UninstPage uninstConfirm
UninstPage instfiles
 
;--------------------------------
 
AutoCloseWindow false
ShowInstDetails show
 
 
; beginning (invisible) section
Section
 
  WriteRegStr HKLM "${regkey}" "Install_Dir" "$INSTDIR"
  ; write uninstall strings
  WriteRegStr HKLM "${uninstkey}" "DisplayName" "${productname} (remove only)"
  WriteRegStr HKLM "${uninstkey}" "UninstallString" '"$INSTDIR\${uninstaller}"'
 
  SetOutPath $INSTDIR
 
 
; package all files, recursively, preserving attributes
; assume files are in the correct places

File /a /r /x "*.nsi" /x "${setupname}" "${srcdir}\*.*" 

WriteUninstaller "${uninstaller}"
  
SectionEnd
 
; create shortcuts
Section
CreateDirectory "${startmenu}"
SetOutPath $INSTDIR ; for working directory
CreateShortCut "${startmenu}\${productname}.lnk" "$INSTDIR\${executable}"
CreateShortCut "${startmenu}\Uninstall.lnk" $INSTDIR\uninstall.exe"
SectionEnd
 
; Uninstaller
; All section names prefixed by "Un" will be in the uninstaller
 
UninstallText "This will uninstall ${productname}."
 
Section "Uninstall"
 
DeleteRegKey HKLM "${uninstkey}"
DeleteRegKey HKLM "${regkey}"

RMDir /r "${startmenu}"
RMDir /r "$INSTDIR"

SectionEnd

