$env:CraftRoot=[System.IO.Path]::GetDirectoryName($myInvocation.MyCommand.Definition)
$env:CraftDeprecatedEntryScript="kdeenv.ps1"
& $env:CraftRoot\craftenv.ps1 "$args"


