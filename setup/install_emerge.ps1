$Script:minPythonVersion = "3.5.0"
$Script:pythonUrl = "https://www.python.org/ftp/python/3.5.1/python-3.5.1.exe"

$Script:installRoot = "C:\kde"
$Script:architecture = "x86"
$Script:compiler = "mingw4"
#####
$Script:python = where.exe python 2>$NULL
$Script:pythonVersion = "0"

function SelectArchitecture()
{
    switch($host.UI.PromptForChoice("Emerge build architecture", "Please select build architecture.",
         @("x&86", "x&64"),
        0))
        {
            0 {
                $Script:architecture = "x86"
                break
            }
            1 {
                $Script:architecture = "x64"
                break
            }
        }
}


function SelectCompiler()
{
    switch($host.UI.PromptForChoice("Emerge compiler", "Please select the compiler.",
         @("&MinGW-w64", "Microsoft &Visual Studio 2015"),
        0))
        {
            0 {
                $Script:compiler = "mingw4"
                break
            }
            1 {
                $Script:compiler = "msvc2015"
                break
            }
        }
}

function FetchPython()
{
    switch($host.UI.PromptForChoice("Get python", "Do you wan't us to isnatll python for you or do you want to manually specify the location of your python installation?",
         @("&Install Python", "&Specify Installation", "&Quit"),
        0))
        {
            0 {
                $installer = "$Script:installRoot\download\{0}" -f ( $Script:pythonUrl.SubString($Script:pythonUrl.LastIndexOf("/")+1))
                if(!(Test-Path -Path $installer))
                {
                    Invoke-WebRequest $Script:pythonUrl -OutFile $installer
                }
                $Script:python = "$Script:installRoot\python\python.exe"
                & "$installer" "/quiet" "InstallAllUsers=0" "TargetDir=$Script:installRoot\python\" "Shortcuts=0" "AssociateFiles=0" "Include_launcher=0"
                break
            }
            1 {
                $Script:python = Read-Host -Prompt "Python Path"
                break
            }
            2 {
                exit
            }
        }
}

function SetSetting([string[]] $ini, [string] $key, [string] $value)
{
    Write-Host ("^\s*{0}\s*=.*`$" -f $key), ("{0} = {1}" -f $key, $value)
    $ini = $ini -replace ("^\s*{0}\s*=.*`$" -f $key), ("{0} = {1}" -f $key, $value)
    return $ini
}

function FetchEmerge()
{
    $Script:emergeTar = "$Script:installRoot\download\emerge.zip"
    if(!(Test-Path -Path $Script:emergeTar))
    {
        Invoke-WebRequest "https://github.com/KDE/emerge/archive/master.zip" -OutFile $Script:emergeTar
    }
    & "$Script:python" "-c" "import shutil; shutil.unpack_archive('$Script:emergeTar','$Script:installRoot')"
    mv "$Script:installRoot\emerge-master" "$Script:installRoot\emerge"
}

function TestPython()
{
    if($Script:python -ne $NULL)
    {  
    if(($Script:python -split "\r\n").Length -eq 1)
        {
            (& "$Script:python" "--version" ) -match "\d.\d.\d" | Out-Null
            $Script:pythonVersion = $Matches[0]    
            if( [int]::Parse($Script:minPythonVersion -replace "\.") -ge [int]::Parse($Script:pythonVersion -replace "\."))
            {
                Write-Host "We found $Script:python version $Script:pythonVersion which is to old."
            }
        }
        else
        {
            Write-Host "We failed to determine your python version."
        }
    }
    else
    {
        Write-Host "We couldn't find python."
    }
}
####################################################
# Start
Write-Host "Start to boostrap emerge."
Write-Host "Where to you want us to install emerge"
$Script:installRoot = if (($result = Read-Host "Emerge install root: [$Script:installRoot]") -eq '') {$Script:installRoot} else {$result}


if(Test-Path -Path $Script:installRoot){
    Write-Host "Directory $Script:installRoot already exists. Exiting."
    exit
}
mkdir $Script:installRoot -Force | Out-Null
mkdir $Script:installRoot\download -Force | Out-Null
mkdir $Script:installRoot\etc -Force | Out-Null

if(!(TestPython))
{
    FetchPython
}
SelectArchitecture
SelectCompiler

FetchEmerge

$iniContent = (Get-Content "$Script:installRoot\emerge\kdesettings.ini")
Write-Host $iniContent.GetType().FullName
$iniContent = SetSetting $iniContent "Python" $Script:python.Substring(0,$Script:python.LastIndexOf("\"))
$iniContent = SetSetting $iniContent "Architecture" $Script:architecture
$iniContent = SetSetting $iniContent "KDECOMPILER" $Script:compiler

[System.IO.File]::WriteAllLines("$Script:installRoot\etc\kdesettings.ini" , $iniContent)
. $Script:installRoot\emerge\kdeenv.ps1
emerge git
rm -Force -Recurse $Script:installRoot\emerge
git clone kde:emerge $Script:installRoot\emerge
cd $Script:installRoot

#############
Write-Host "You are ready to go!"
Write-Host "Type `"emerge openssl`" to build your firts application."