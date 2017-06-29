$env:CraftRoot=[System.IO.Path]::GetDirectoryName($myInvocation.MyCommand.Definition)
$env:CraftDeprecatedEntryScript="kdeenv.ps1"
if ($args) {
    & $env:CraftRoot\craftenv.ps1 "$args"
} else {
   & $env:CraftRoot\craftenv.ps1
}
