
#      this file sets some environment variables that are needed
#    for finding programs and libraries etc.
#    by Holger Schroeder <schroder@kde.org>
#    by Patrick Spendrin <ps_ml@gmx.de>

#    you should copy kdesettings-example.bat to ..\etc\kdesettings.bat
#    and adapt it to your needs (see that file for more info)

#    this file should contain all path settings - and provide thus an environment
#    to build and run kde programs
#    this file sources the kdesettings.bat file automatically

cls

$dp0=[System.IO.Path]::GetDirectoryName($myInvocation.MyCommand.Definition)

&{

 $env:EMERGE_BUILDTYPE="RelWithDebInfo"

foreach($arg in $args)
{
if($arg.ToString().ToLower() -is  @("debug","release","relwithdebinfo"))
{
    $env:EMERGE_BUILDTYPE=$arg
}
else
{
    $APPLICATION=$arg
}

}
function subst([string] $varname, [string] $path, [string] $drive)
{
    foreach($key in $settings["Paths"].keys)
    {
        $path = $path.Replace("`$`{"+$key+"`}",$settings["Paths"][$key])
    }
    if(!(test-path -path $path))
    {
        mkdir $path
    }

    if( $settings["ShortPath"]["EMERGE_USE_SHORT_PATH"] -eq $true )
    {
        if(!(test-path -path $drive))
        {
            subst.exe $drive $path
        }
        $path=$drive
    }
    if(!$path.endswith("\"))
    {
        $path += "\"
    }
    [Environment]::SetEnvironmentVariable($varname, $path, "Process")
    
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



if(test-path -path $dp0\..\etc\kdesettings.ini)
{
    $settings = readINI $dp0\..\etc\kdesettings.ini
}
else
{
    Write-Error("$dp0\..\etc\kdesettings.ini Does not exist")
}


#make settings for general availible in env
foreach($key in $settings["General"].keys)
{
    [Environment]::SetEnvironmentVariable($key,$settings["General"][$key], "Process")
}


subst "KDEROOT" $settings["Paths"]["KDEROOT"] $settings["ShortPath"]["EMERGE_ROOT_DRIVE"]
subst "DOWNLOADDIR" $settings["Paths"]["DOWNLOADDIR"] $settings["ShortPath"]["EMERGE_DOWNLOAD_DRIVE"]
subst "KDESVNDIR" $settings["Paths"]["KDESVNDIR"] $settings["ShortPath"]["EMERGE_SVN_DRIVE"]
subst "KDEGITDIR" $settings["Paths"]["KDEGITDIR"] $settings["ShortPath"]["EMERGE_GIT_DRIVE"]



function path-mingw()
{
    if(test-path -path "$env:KDEROOT\mingw\bin")
    {
        $env:PATH="$env:KDEROOT\mingw\bin;$env:PATH"
    }
    else 
    {
        if(test-path -path "$env:KDEROOT\mingw64\bin")
        {
            $env:PATH="$env:KDEROOT\mingw64\bin;$env:PATH"
        }
        else
        { #dont know which version
             $env:PATH="$env:KDEROOT\mingw64\bin;$env:KDEROOT\mingw\bin;$env:PATH"
        }
    }
}

if ($settings["General"]["KDECOMPILER"] -eq "mingw4")
{ 
    path-mingw
}



$env:PATH="$env:KDEROOT\bin;$env:PATH"
$env:QT_PLUGIN_PATH="$env:KDEROOT\plugins;$env:KDEROOT\lib\kde4\plugins"
$env:XDG_DATA_DIRS="$env:KDEROOT\share"

# for emerge
$env:PATH="$env:KDEROOT\emerge\bin;$env:PATH"

# for dev-utils
$env:PATH="$env:KDEROOT\dev-utils\bin;$env:PATH"

$env:PATH="$env:KDEROOT\bin;$env:PATH"
#todo:get pythonpath from registry
$env:PATH="$env:PATH;"+$settings["Paths"]["PYTHONPATH"]

$env:HOME=$env:USERPROFILE
$env:SVN_SSH="plink"
$env:GIT_SSH="plink"


Write-Host("KDEROOT     : ${env:KDEROOT}")
Write-Host("KDECOMPILER : ${env:KDECOMPILER}")
Write-Host("KDESVNDIR   : ${env:KDESVNDIR}")
Write-Host("KDEGITDIR   : ${env:KDEGITDIR}")
Write-Host("PYTHONPATH  : " + $settings["Paths"]["PYTHONPATH"])
Write-Host("DOWNLOADDIR : ${env:DOWNLOADDIR}")

}

function emerge()
{
    python "$env:KDEROOT\emerge\bin\emerge.py" $args
}

cd $env:KDEROOT
