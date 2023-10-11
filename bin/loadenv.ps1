# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Hannah von Reth <vonreth@kde.org>

$craftenvJson = [IO.Path]::GetFullPath("{0}/../../etc/craftenv.json" -f [System.IO.Path]::GetDirectoryName($myInvocation.MyCommand.Definition))

if(-not (Test-Path $craftenvJson)) {
    Write-Host "$craftenvJson does not exist, please run craftenv.ps1 first"
    return
}

$craftEnv = Get-Content $craftenvJson | ConvertFrom-Json
# clear the current env
Get-ChildItem env: | ForEach-Object {
    Remove-Item ("ENV:{0}" -f ${_}.Name)
}

# repopulate it with the content from craftenv.json
foreach ($property in $craftEnv.PSObject.Properties) {
    Set-Item -force -path "ENV:\$($property.Name)"  -value "$($property.Value)"
}