$Script:minPythonVersion = "3.5.0"
$Script:pythonUrl = "https://www.python.org/ftp/python/3.5.1/python-3.5.1.exe"

$Script:installRoot = "C:\kde"
#####
$Script:python = where.exe python 2>$NULL
$Script:pythonVersion = "0"

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

function FetchEmerge()
{
    $Script:emergeTar = "$Script:installRoot\download\emerge.zip"
    if(!(Test-Path -Path $Script:emergeTar))
    {
        Invoke-WebRequest "https://github.com/KDE/emerge/archive/master.zip" -OutFile $Script:emergeTar
    }
    & "$Script:python" "-c" "import shutil; shutil.unpack_archive('$Script:emergeTar','$Script:installRoot')"
    mv "$Script:installRoot\emerge-master" "$Script:installRoot\emerge"
    $content = (Get-Content "$Script:installRoot\emerge\kdesettings.ini") -replace "^Python = .*`$", ("Python = {0}" -f $Script:python.Substring(0,$Script:python.LastIndexOf("\"))) 
    [System.IO.File]::WriteAllLines("$Script:installRoot\etc\kdesettings.ini" , $content)
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

if($Script:python -ne $NULL)
{
    (& "$Script:python" "--version") -match "\d.\d.\d" | Out-Null
    $Script:pythonVersion = $Matches[0]    
    if( [int]::Parse($Script:minPythonVersion -replace "\.") -ge [int]::Parse($Script:pythonVersion -replace "\."))
    {
        Write-Host "We found $Script:python version $Script:pythonVersion which is to old."
        FetchPython
    }
}
else
{
    Write-Host "We couldn't find python."
    FetchPython
}

FetchEmerge
. $Script:installRoot\emerge\kdeenv.ps1
emerge git
rm -Force -Recurse $Script:installRoot\emerge
git clone kde:emerge $Script:installRoot\emerge
cd $Script:installRoot