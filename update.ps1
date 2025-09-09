$files = git ls-files --full-name *.py *.ini

function update-sed {
    param (
        [string[]]$pattern,
        [string[]]$files
    )
    if (-not $pattern) {
        return
    }
    $files | ForEach-Object -Parallel {
        $sed = "sed"
        if ($IsMacOS) {
            $sed = "gsed"
        }
        $path = (Join-Path ${PWD} ${_})
        $command = @("-i") + @using:pattern + @(${path})
        #Write-Host "Applying pattern: ${sed} ${command}"
        & ${sed} @command
        exit
    }
}
# TODO: combine multiple patterns per call to sed
$patterns = @()
Get-Content ${PSScriptRoot}/replacements.txt | ForEach-Object {
    if ($_)
    {
        $patterns += @("-e", $_)

        if ($patterns.Length -ge 20)
        {
            update-sed $patterns -files $files
            $patterns = @() # reset patterns
        }
    }
}
update-sed $patterns -files $files
