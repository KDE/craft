param(
    [alias("root")][string]$Script:installRoot=$null,
    [alias("python")][string]$Script:python=$null,
    [string[]]$Script:extraArgs
    )


$Script:minPythonVersion = "3.5.0"
if($env:PROCESSOR_ARCHITECTURE.contains("64"))
{
    $Script:pythonUrl = "https://www.python.org/ftp/python/3.5.1/python-3.5.1-embed-amd64.zip"
}
else
{
    $Script:pythonUrl = "https://www.python.org/ftp/python/3.5.1/python-3.5.1-embed-win32.zip"
}
#####
$Script:pythonVersion = "0"

function FetchPython()
{
    switch($host.UI.PromptForChoice("Get python", "Do you wan't us to install python for you or do you want to manually specify the location of your python installation?",
         @("&Install Python", "&Specify Installation", "&Quit"),
        0))
        {
            0 {
                $archive = "$Script:installRoot\download\{0}" -f ( $Script:pythonUrl.SubString($Script:pythonUrl.LastIndexOf("/")+1))
                if(!(Test-Path -Path $archive))
                {
                    Invoke-WebRequest $Script:pythonUrl -OutFile $archive
                }
                $Script:python = "$Script:installRoot\python\python.exe"
                Expand-Archive "$archive" "$Script:installRoot\python\"
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
if ($Script:installRoot -eq $null) {
    Write-Host "Where to you want us to install emerge"
    $Script:installRoot="C:\KDE\"
    $Script:installRoot = if (($result = Read-Host "Emerge install root: [$Script:installRoot]") -eq '') {$Script:installRoot} else {$result}
}


while(Test-Path -Path $Script:installRoot){
    Write-Host "Directory $Script:installRoot already exists.`nChoose one of the options:"
	switch($ask=Read-Host "[Q] Quit installation    `n[Y] Truncate directory: [$Script:installRoot] and continue installation in the same directory    `n[N] Change directory path.`n(default is 'Q')")
	{
		"y"		{rmdir $Script:installRoot}
		"n"		{$Script:installRoot=if (($result = Read-Host "Enter another directory to install emerge (default is ["$Script:installRoot"(1)])") -eq '') {$Script:installRoot+"(1)"} else {$result}}
		"q"		{exit}
		default	{exit}
	}
}

mkdir $Script:installRoot -Force | Out-Null
mkdir $Script:installRoot\download -Force | Out-Null

if ($Script:python -eq $null) {
    $Script:python= (where.exe python 2>$null)
    TestAndFetchPython
}

(new-object net.webclient).DownloadFile("https://raw.githubusercontent.com/KDE/emerge/master/setup/EmergeBootstrap.py", "$Script:installRoot\download\EmergeBootstrap.py")

Start-Sleep -s 10
Write-Host "$Script:python" "$Script:installRoot\download\EmergeBootstrap.py" --root "$Script:installRoot" "$Script:extraArgs"
& "$Script:python" "$Script:installRoot\download\EmergeBootstrap.py" --root "$Script:installRoot" $Script:extraArgs
cd $Script:installRoot
