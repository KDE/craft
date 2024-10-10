#    this file sets some environment variables that are needed
#    for finding programs and libraries etc.
#    by Hannah von Reth <vonreth@kde.org>
#    you should copy CraftSettings.ini.template to ..\etc\CraftSettings.ini
#    and adapt it to your needs (see that file for more info)

cls

$env:CraftRoot=[System.IO.Path]::GetDirectoryName($myInvocation.MyCommand.Definition)

&{
[version]$minPythonVersion = '3.9'

function findPython([string] $name)
{
    if ($env:CRAFT_PYTHON -and (Test-Path -path $env:CRAFT_PYTHON)) {
        return
    }
    $py = (Get-Command $name -ErrorAction SilentlyContinue)
    if ($py) {
        if (($py | Get-Member Version) -and $py.Version -ge $minPythonVersion) {
            $env:CRAFT_PYTHON=$py.Source
        } elseif ((& $py --version) -match 'Python (?<version>[\d.]+)' -and [version]$Matches['version'] -ge $minPythonVersion) {
            $env:CRAFT_PYTHON=$py.Source
        }
    }
}

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


if(test-path -path $env:CraftRoot\..\etc\kdesettings.ini)
{
    mv $env:CraftRoot\..\etc\kdesettings.ini $env:CraftRoot\..\etc\CraftSettings.ini
}

if(test-path -path $env:CraftRoot\..\etc\CraftSettings.ini)
{
    $settings = readINI $env:CraftRoot\..\etc\CraftSettings.ini
}
else
{
    Write-Error("$env:CraftRoot\..\etc\CraftSettings.ini Does not exist")
    break
}

if($settings["Paths"].Contains("Python") -and (Test-Path -path $settings["Paths"]["Python"]))
{
    # prefer the python from the settings
    findPython("{0}/python" -f $settings["Paths"]["Python"])
}

findPython("python3.12")
findPython("python3.11")
findPython("python3.10")
findPython("python3.9")
findPython("python3")
findPython("python")
findPython("py")
}

function Global:craft()
{
    $python = (Get-Command "$env:KDEROOT/dev-utils/bin/python3" -ErrorAction SilentlyContinue).Source
    if (-not $python) {
        $python = $env:CRAFT_PYTHON
    }
    return & $python ([IO.PATH]::COMBINE("$env:CraftRoot", "bin", "craft.py")) @args
}

function Global:craftCd([string] $package, [string]$property, [string] $target="")
{
    $command = @()
    if ($target) {
        $command += @("--target", $target)
    }
    $command += @("-q", "--ci-mode", "--get", $property, $package)
    $dir = craft @command | Out-String
    if($LASTEXITCODE) {
        Write-Host $dir
    } else {
        cd "$dir".Trim()
    }
}


function Global:cb([string] $package, [string] $target="")
{
    craftCd $package "buildDir()" $target
}

function Global:cs([string] $package, [string] $target="")
{
    craftCd $package "sourceDir()" $target
}

function Global:ci([string] $package, [string] $target="")
{
    craftCd $package "imageDir()" $target
}

function Global:cr()
{
    cd $env:CraftRoot/..
}

if (-not $env:CRAFT_PYTHON) {
    Write-Error "Failed to detect python"
    exit(1)
}

if($args.Length -ne 0)
{
    craft --run @args
} else {
    $env2 = ConvertFrom-Json (& $env:CRAFT_PYTHON ([IO.PATH]::COMBINE("$env:CraftRoot", "bin", "CraftSetupHelper.py")) @("--setup", "--format=json"))
    Get-ChildItem env: | ForEach-Object {
        Remove-Item ("ENV:{0}" -f ${_}.Name)
    }
    foreach ($property in $env2.PSObject.Properties) {
        Set-Item -force -path "ENV:\$($property.Name)"  -value "$($property.Value)"
    }
    cr
}

