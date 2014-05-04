
#    this file sets some environment variables that are needed
#    for finding programs and libraries etc.
#    by patrick von Reth <vonreth@kde.org>
#    you should copy kdesettings.ini to ..\etc\kdesettings.ini
#    and adapt it to your needs (see that file for more info)

#    this file should contain all path settings - and provide thus an environment
#    to build and run kde programs
#    based on kdeenv.bat

cls


$EMERGE_ROOT=[System.IO.Path]::GetDirectoryName($myInvocation.MyCommand.Definition)

$EMERGE_ARGUMENTS = $args

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
}

function prependPATH([string] $path)
{
    $env:PATH="$path;$env:PATH"
}


if( $EMERGE_ARGUMENTS[0] -eq "--get")
{
    Write-Host($settings[$EMERGE_ARGUMENTS[1]][$EMERGE_ARGUMENTS[2]])
    break
}
prependPATH $settings["Paths"]["PYTHONPATH"]

python "$EMERGE_ROOT\bin\emerge_setup_helper.py" "--subst"


$EMERGE_ENV = (python "$EMERGE_ROOT\bin\emerge_setup_helper.py" "--getenv") | 
foreach {
  if ($_ -match "=") {        
    $v = $_.split("=")
    set-item -force -path "ENV:\$($v[0])"  -value "$($v[1])"
    #Write-Host("$v[0]=$v[1]")
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



if(([string]$settings["General"]["KDECOMPILER"]).StartsWith("msvc"))
{
    path-msvc
}


(python "$EMERGE_ROOT\bin\emerge_setup_helper.py" "--print-banner")

cd "$env:KDEROOT"
}


function emerge()
{
    python "$env:KDEROOT\emerge\bin\emerge.py" $args
}


# make sure term is not defined by any script
$env:TERM=""
$EMERGE_ARGUMENTS=$null

if($args.Length -eq 2 -and $args[0] -eq "--package")
{
    python "$env:KDEROOT\emerge\server\package.py" $args[1]
}
else
{
    if($args.Length -ne 0)
    {
        invoke-expression -command "$args"
    }

}