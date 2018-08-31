!define PowerShell "$WINDIR\sysnative\WindowsPowerShell\v1.0\powershell.exe -NoProfile -ExecutionPolicy ByPass -Command"

Var ProcessList

!macro StopProcess root
    nsExec::ExecToLog '${PowerShell} "&{ Write-Host \"Killing processes in\" (Join-Path \"${root}\" *); Get-Process * | Where-Object { $$_.Path -Like (Join-Path \"${root}\" *) } |  %{ Write-Host \"killing\", $$_.Path; Stop-Process $$_ } }"'
!macroend


!macro ListProcess root
    nsExec::ExecToStack '${PowerShell} "&{ Get-Process * | Where-Object { $$_.Path -Like (Join-Path \"${root}\" *) } |  %{ Write-Host $$_.Path } }"'
    Pop $0
    Pop $1
    StrCpy $ProcessList $1
!macroend


!macro EndProcessWithDialog
retry_kil:
    !insertmacro ListProcess "$INSTDIR"
    ${If} $ProcessList != ""
        MessageBox MB_YESNOCANCEL "You have $\n$ProcessList running in $INSTDIR.$\n Select $\"Yes$\" to kill the process(es), $\"No$\" to retry or $\"Cancel$\" to quit." /SD IDYES IDNO retry_kil IDCANCEL abort_kill
        !insertmacro StopProcess "$INSTDIR"
        Goto retry_kil
        abort_kill:
            Quit
    ${EndIf}
!macroend
