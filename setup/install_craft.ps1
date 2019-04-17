param(
    [alias("root")][string]$Script:installRoot=$null,
    [alias("python")][string]$Script:python=$null,
    [alias("branch")][string]$Script:branch="master",
    [alias("localdev")][string]$Script:localdev=$null
    )
    
[Net.ServicePointManager]::SecurityProtocol = "SystemDefault, tls12, tls11"
[version]$minPythonVersion = 3.6
$Script:PythonInstallDir = "C:\python36"

if($env:PROCESSOR_ARCHITECTURE.contains("64"))
{
    $Script:pythonUrl = "https://www.python.org/ftp/python/3.6.6/python-3.6.6-amd64.exe"
}
else
{
    $Script:pythonUrl = "https://www.python.org/ftp/python/3.6.6/python-3.6.6.exe"
}
#####
$Script:pythonVersion = "0"

function findPython([string] $name)
{
    $py = (Get-Command $name -ErrorAction SilentlyContinue)
    if ($py -and ($py | Get-Member Version) -and $py.Version -ge $minPythonVersion) {
        return $py.Source
    }
    return $null
}

function FetchPython()
{
    switch($host.UI.PromptForChoice("Get python", "Do you want us to install python for you or do you want to manually specify the location of your python installation?",
         @("&Install Python", "&Specify Installation", "&Quit"),
        0))
        {
            0 {
                $archive = "$Script:installRoot\download\{0}" -f ( $Script:pythonUrl.SubString($Script:pythonUrl.LastIndexOf("/")+1))
                if(!(Test-Path -Path $archive))
                {
                    Write-Host "Downloading:" $Script:pythonUrl
                    (new-object net.webclient).DownloadFile("$Script:pythonUrl", "$archive")
                }
                [string[]]$command = @("/quiet", "InstallAllUsers=0", "PrependPath=1", "TargetDir=`"$Script:PythonInstallDir`"", "AssociateFiles=0",  "InstallLauncherAllUsers=0")
                Write-Host "$archive" $command
                & "$archive" $command
                $Script:python = "$Script:PythonInstallDir\python.exe"
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
    if($Script:python)
    {
        if(($Script:python -split "\r\n").Length -eq 1)
        {
            Try {
                (& "$Script:python" "--version" 2>&1) -match "\d.\d.\d" | Out-Null
                $Script:pythonVersion = $Matches[0]
                if([version]$Script:pythonVersion -ge $minPythonVersion)
                {
                    return
                }
                Write-Host "We found $Script:python version $Script:pythonVersion which is to old."
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
Write-Host "Start to boostrap Craft."
function promptInstallRoot()
{
    Write-Host "Where to you want us to install Craft"
    $Script:installRoot="C:\CraftRoot\"
    $Script:installRoot = if (($result = Read-Host "Craft install root: [$Script:installRoot]") -eq '') {$Script:installRoot} else {$result}
}

if (!$Script:installRoot) {
    promptInstallRoot
}

while(Test-Path -Path $Script:installRoot\*){
    Write-Host "Directory $Script:installRoot already exists.`nChoose one of the options:"
	switch($ask=Read-Host "[Q] Quit installation    `n[Y] Truncate directory: [$Script:installRoot] and continue installation in the same directory    `n[N] Change directory path.`n(default is 'Q')")
	{
		"y"		{rm $Script:installRoot\* -Force}
		"n"		{promptInstallRoot}
		"q"		{exit}
	}
}

mkdir $Script:installRoot -Force | Out-Null
mkdir $Script:installRoot\download -Force | Out-Null

if (!$Script:python) {
    $Script:python = findPython("python")
    if (!$Script:python) {
        $py = (Get-Command py -ErrorAction SilentlyContinue).Name
        if ($py) {
            $Script:python = findPython(&$py -3 -c "import sys; print(sys.executable)")
        }
        if (!$Script:python) {
            $Script:python=(where.exe python 2>$null)
        }
    }
    TestAndFetchPython
}
&{
if ($Script:localdev) {
Copy-Item "$Script:localdev\Setup\CraftBootstrap.py" -Dest "$Script:installRoot\download\CraftBootstrap.py"
Write-Host "Copied local CraftBootstrap.py"
} else {
$url = "https://raw.githubusercontent.com/KDE/craft/$Script:branch/setup/CraftBootstrap.py"
Write-Host "Downloading:" $url
(new-object net.webclient).DownloadFile("$url", "$Script:installRoot\download\CraftBootstrap.py")

Start-Sleep -s 10
}
[string[]]$command = @("$Script:installRoot\download\CraftBootstrap.py", "--prefix", "$Script:installRoot", "--branch", "$Script:branch")
if ($Script:localdev) {
   [string[]]$command += @("--localDev", $Script:localdev)
}
Write-Host "$Script:python" $command
& "$Script:python" $command
cd $Script:installRoot
}
