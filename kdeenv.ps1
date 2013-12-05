
#    this file sets some environment variables that are needed
#    for finding programs and libraries etc.
#    by patrick von Reth <vonreth@kde.org>
#    you should copy kdesettings.ini to ..\etc\kdesettings.ini
#    and adapt it to your needs (see that file for more info)

#    this file should contain all path settings - and provide thus an environment
#    to build and run kde programs
#    based on kdeenv.bat

cls

$dp0=[System.IO.Path]::GetDirectoryName($myInvocation.MyCommand.Definition)

&{

function subst([string] $varname, [string] $path, [string] $drive)
{
	while($path.Contains("$"))
	{
		foreach($key in $settings["Paths"].keys)
		{
			$path = $path.Replace("`$`{"+$key+"`}",$settings["Paths"][$key])
		}
	}
    if(!(test-path -path $path))
    {
        mkdir $path
    }

    if( $settings["ShortPath"]["EMERGE_USE_SHORT_PATH"] -eq $true )
    {
        [Environment]::SetEnvironmentVariable("EMERGE_USE_SHORT_PATH",$settings["ShortPath"]["EMERGE_USE_SHORT_PATH"],"Process")
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

function prependPATH([string] $path)
{
    $env:PATH="$path;$env:PATH"
}

function path-mingw()
{
    if(test-path -path "$env:KDEROOT\mingw\bin")
    {
        prependPATH "$env:KDEROOT\mingw\bin"
    }
    else 
    {
        if(test-path -path "$env:KDEROOT\mingw64\bin")
        {
            prependPATH "$env:KDEROOT\mingw64\bin"
        }
        else
        { 
            #dont know which version
            prependPATH "$env:KDEROOT\mingw64\bin"
            prependPATH "$env:KDEROOT\mingw\bin"
        }
    }
}

function setupMSVCENV([string] $key)
{
    $path = [Environment]::GetEnvironmentVariable($key, "Process")
    if($path  -eq "")
        {
            Write-Host("Couldnt find msvc installation")
        }
        #http://stackoverflow.com/questions/2124753/how-i-can-use-powershell-with-the-visual-studio-command-prompt
        $arch = "x86"
        if($settings["General"]["EMERGE_ARCHITECTURE"] -eq "x64")
        {
            $arch = "amd64"
        }        
        pushd "$path\..\..\VC"
        cmd /c "vcvarsall.bat $arch &set" |
        foreach {
          if ($_ -match "=") {        
            $v = $_.split("=")
            set-item -force -path "ENV:\$($v[0])"  -value "$($v[1])"
            #Write-Host("$v[0]=$v[1]")
          }
        }
        popd
}
function path-msvc()
{
    if($settings["General"]["KDECOMPILER"] -eq "msvc2010")
    {
       setupMSVCENV "VS100COMNTOOLS"
    }
    if($settings["General"]["KDECOMPILER"] -eq "msvc2012")
    {
       setupMSVCENV "VS110COMNTOOLS"
    }
    if($settings["General"]["KDECOMPILER"] -eq "msvc2013")
    {
       setupMSVCENV "VS120COMNTOOLS"
    }
    
}

function setupCCACHE()
{
    if( $settings["General"]["EMERGE_USE_CCACHE"] -eq $true)
    {
        $env:CCACHE_DIR="$env:KDEROOT\build\CCACHE"
    }
}


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



if ($settings["General"]["KDECOMPILER"] -eq "mingw4")
{ 
    path-mingw
    setupCCACHE
}
else
{
    if(([string]$settings["General"]["KDECOMPILER"]).StartsWith("msvc"))
    {
        path-msvc
    }
}


$env:QT_PLUGIN_PATH="$env:KDEROOT\plugins;$env:KDEROOT\lib\kde4\plugins"
$env:XDG_DATA_DIRS="$env:KDEROOT\share"

# for dev-utils
prependPATH  "$env:KDEROOT\dev-utils\bin"

#todo:get pythonpath from registry
prependPATH $settings["Paths"]["PYTHONPATH"]

# make sure that kderoot/bin is the last in path to prevent issues wer libs from devutils are used
prependPATH "$env:KDEROOT\bin"

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

# make sure term is not defined by any script
$env:TERM=""