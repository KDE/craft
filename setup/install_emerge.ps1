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
                if(!($Script:python.EndsWith(".exe")))
                {
                    $Script:python = "$Script:python\python.exe"
                }
                TestAndFetchPython
                break
            }
            2 {
                exit
            }
        }
}

function TestAndFetchPython()
{
    if($Script:python -ne $NULL)
    {  
        if(($Script:python -split "\r\n").Length -eq 1)
        {
            Try {
                (& "$Script:python" "--version" ) -match "\d.\d.\d" | Out-Null
                $Script:pythonVersion = $Matches[0]
                if( [int]::Parse($Script:minPythonVersion -replace "\.") -ge [int]::Parse($Script:pythonVersion -replace "\."))
                {
                    Write-Host "We found $Script:python version $Script:pythonVersion which is to old."
                }
                else
                {
                    return
                }
            }
            Catch {
                Write-Host "We failed to determine your python version."
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
    FetchPython
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

TestAndFetchPython

(new-object net.webclient).DownloadFile("https://raw.githubusercontent.com/KDE/emerge/master/setup/EmergeBootstrap.py", "$Script:installRoot\download\EmergeBootstrap.py")

Start-Sleep -s 10
& "$Script:python" "$Script:installRoot\download\EmergeBootstrap.py" "$Script:installRoot"
cd $Script:installRoot
