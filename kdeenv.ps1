
#    this file sets some environment variables that are needed
#    for finding programs and libraries etc.
#    by Hannah von Reth <vonreth@kde.org>
#    you should copy kdesettings.ini to ..\etc\kdesettings.ini
#    and adapt it to your needs (see that file for more info)

#    this file should contain all path settings - and provide thus an environment
#    to build and run kde programs
#    based on kdeenv.bat

cls


$EMERGE_ROOT=[System.IO.Path]::GetDirectoryName($myInvocation.MyCommand.Definition)

$EMERGE_ARGUMENTS = $args

$env:EMERGE_PYTHON = (Get-Command python3 -ErrorAction SilentlyContinue).Source

if( -Not $env:EMERGE_PYTHON)
{
    $env:EMERGE_PYTHON = (Get-Command python -ErrorAction SilentlyContinue).Source
}

&{
function readINI([string] $fileName)
{
   $ini = @{}

  switch -regex -file $fileName {
    "^\[(.+)\]$" {
      $section = $matches[1].Trim()
      $ini[$section] = @{}
    }
    "^\s*([^#].+?)\s*=\s*(.*)" {
      $name,$value = $matches[1..2]
      $ini[$section][$name] = $value.Trim()
    }
  }
  $ini
}



if(test-path -path $EMERGE_ROOT\..\etc\kdesettings.ini)
{
    $settings = readINI $EMERGE_ROOT\..\etc\kdesettings.ini
}
else
{
    Write-Error("$EMERGE_ROOT\..\etc\kdesettings.ini Does not exist")
    break
}
if( $EMERGE_ARGUMENTS[0] -eq "--get")
{
    Write-Host($settings[$EMERGE_ARGUMENTS[1]][$EMERGE_ARGUMENTS[2]])
    break
}


function prependPATH([string] $path)
{
    $env:PATH="$path{0}$env:PATH" -f [IO.Path]::PathSeparator
}


if( -Not $env:EMERGE_PYTHON)
{
    prependPATH $settings["Paths"]["Python"]
    $env:EMERGE_PYTHON = ("{0}{1}python" -f $settings["Paths"]["Python"], [IO.Path]::PathSeparator)
}

(& $env:EMERGE_PYTHON ([IO.PATH]::COMBINE("$EMERGE_ROOT", "bin", "EmergeSetupHelper.py")) "--setup" "--mode" "powershell") |
foreach {
  if ($_ -match "=") {
    $v = $_.split("=")
    set-item -force -path "ENV:\$($v[0])"  -value "$($v[1])"
    #Write-Host("$v[0]=$v[1]")
  }
}

cd "$env:KDEROOT"
}


function Global:emerge() {
    return & $env:EMERGE_PYTHON ([IO.PATH]::COMBINE("$env:KDEROOT", "emerge", "bin", "emerge.py")) $args
}


$EMERGE_ARGUMENTS=$null

if($args.Length -eq 2 -and $args[0] -eq "--package")
{
    & $env:EMERGE_PYTHON ([IO.PATH]::COMBINE("$env:KDEROOT", "emerge", "server", "package.py")) $args[1]
}
else
{
    if($args.Length -ne 0)
    {
        invoke-expression -command "$args"
    }

}
