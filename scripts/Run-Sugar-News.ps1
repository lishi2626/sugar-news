<#
.SYNOPSIS
    Build, publish and verify Sugar News dashboard.
#>

param(
    [string]$Date,
    [string]$TaskRoot,
    [string]$VercelBaseUrl = $env:SUGAR_NEWS_BASE_URL,
    [switch]$SkipIfSuccess,
    [switch]$SkipGitSync,
    [switch]$AllowRssAutogen
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
$env:PYTHONIOENCODING = "utf-8"
$env:TZ = "Asia/Shanghai"
$pathCandidates = @(
    "C:\Program Files\Git\cmd",
    "C:\Program Files\nodejs",
    (Join-Path $env:APPDATA "npm")
) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }
if ($pathCandidates) {
    $env:Path = (($pathCandidates + @($env:Path)) -join ";")
}

if (-not $TaskRoot) {
    $TaskRoot = $ProjectRoot
}

$GitNoMaintenanceArgs = @("-c", "gc.auto=0", "-c", "maintenance.auto=false")
$GitNoPromptArgs = @("-c", "credential.interactive=false") + $GitNoMaintenanceArgs

$LogRoot = Join-Path $ProjectRoot "logs"
if (-not (Test-Path -LiteralPath $LogRoot)) {
    New-Item -ItemType Directory -Force -Path $LogRoot | Out-Null
}
$LogDate = Get-Date -Format "yyyyMMdd"
$TaskLog = Join-Path $LogRoot "sugar_news_$LogDate.log"

function Write-Step {
    param([string]$Message)
    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Message"
}

function Get-PythonExe {
    $VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $VenvPython) { return $VenvPython }
    return "python"
}

function Get-BeijingYesterday {
    return ([DateTimeOffset]::UtcNow.ToOffset([TimeSpan]::FromHours(8)).Date.AddDays(-1).ToString("yyyy-MM-dd"))
}

function Invoke-External {
    param(
        [string]$Label,
        [scriptblock]$Command,
        [int]$Attempts = 1
    )
    for ($i = 1; $i -le $Attempts; $i++) {
        & $Command
        if ($LASTEXITCODE -eq 0) { return }
        if ($i -eq $Attempts) {
            throw "$Label failed with exit code $LASTEXITCODE"
        }
        Write-Step "$Label failed with exit code $LASTEXITCODE; retrying ($i/$Attempts)"
        Start-Sleep -Seconds ([Math]::Min(120, 20 * $i))
    }
}

function Get-GeneratedCommitPaths {
    return @("public/sugar-news", "data", "reports", "logs")
}

function Save-GeneratedWorkingTreeChanges {
    if (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot ".git"))) {
        return
    }

    $paths = Get-GeneratedCommitPaths
    $status = & git @GitNoMaintenanceArgs status --porcelain -- @paths
    if (-not $status) {
        return
    }

    $message = "auto-stash Sugar News generated artifacts before daily sync $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Write-Step "Stash generated local changes before git sync"
    & git @GitNoMaintenanceArgs stash push --include-untracked -m $message -- @paths
    if ($LASTEXITCODE -ne 0) {
        throw "git stash failed before remote sync"
    }
}

function Sync-GitRemote {
    if ($SkipGitSync) {
        Write-Step "Git sync skipped by parameter."
        return
    }
    if (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot ".git"))) {
        Write-Step "No git repository found; skipping git sync."
        return
    }

    Save-GeneratedWorkingTreeChanges
    Write-Step "Sync local repository with origin/main"
    Invoke-External -Label "git fetch origin/main" -Attempts 3 -Command {
        & git @GitNoPromptArgs fetch --no-tags origin main
    }
    Invoke-External -Label "git fast-forward origin/main" -Attempts 1 -Command {
        & git @GitNoMaintenanceArgs merge --ff-only origin/main
    }
}

function Invoke-RemoteVerify {
    param([string]$TargetDate)
    if (-not $VercelBaseUrl) {
        Write-Step "SUGAR_NEWS_BASE_URL is not set; skipping remote Vercel verification."
        return
    }
    for ($i = 1; $i -le 18; $i++) {
        try {
            & (Get-PythonExe) scripts/verify_sugar_news_dashboard.py --date $TargetDate --base-url $VercelBaseUrl
            if ($LASTEXITCODE -eq 0) { return }
        } catch {
            Write-Step "Vercel not ready yet (attempt $i/18): $($_.Exception.Message)"
        }
        Start-Sleep -Seconds 20
    }
    throw "Vercel Sugar News verification failed after retry window."
}

Start-Transcript -Path $TaskLog -Append | Out-Null
try {
    if (-not $Date) {
        $Date = Get-BeijingYesterday
    }

    Sync-GitRemote

    Write-Step "Build Sugar News for $Date using task root: $TaskRoot"
    $args = @("scripts/sugar_news_pipeline.py", "--date", $Date, "--task-root", $TaskRoot)
    if ($SkipIfSuccess) { $args += "--skip-if-success" }
    if ($AllowRssAutogen) { $args += "--allow-rss-autogen" }
    & (Get-PythonExe) @args
    if ($LASTEXITCODE -ne 0) {
        throw "sugar_news_pipeline.py failed with exit code $LASTEXITCODE"
    }

    Write-Step "Verify local Sugar News dashboard data"
    & (Get-PythonExe) scripts/verify_sugar_news_dashboard.py --date $Date
    if ($LASTEXITCODE -ne 0) {
        throw "Local Sugar News dashboard verification failed"
    }

    Write-Step "Commit and push Sugar News changes"
    $datedLogRoot = Join-Path "logs" ($Date.Substring(0, 4))
    $commitPaths = @("public/sugar-news", "data", "reports")
    if (Test-Path -LiteralPath (Join-Path $ProjectRoot $datedLogRoot)) {
        $commitPaths += $datedLogRoot
    }
    $status = & git @GitNoMaintenanceArgs status --porcelain -- @commitPaths
    $ahead = & git @GitNoMaintenanceArgs status -sb | Select-String -Pattern "\[ahead [0-9]+\]"
    if ($status) {
        & git @GitNoMaintenanceArgs add -- @commitPaths
        & git @GitNoMaintenanceArgs commit -m "Update Sugar News $Date"
        if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
    }
    if ($status -or $ahead) {
        for ($i = 1; $i -le 12; $i++) {
            Write-Step "git push attempt $i/12"
            & git @GitNoPromptArgs push
            if ($LASTEXITCODE -eq 0) { break }
            if ($i -eq 12) { throw "git push failed after retries" }
            Start-Sleep -Seconds ([Math]::Min(300, 30 * $i))
        }
    } else {
        Write-Step "No Sugar News changes to push"
    }

    Write-Step "Verify Vercel Sugar News page"
    Invoke-RemoteVerify -TargetDate $Date
    Write-Step "Sugar News workflow complete for $Date"
}
finally {
    Stop-Transcript | Out-Null
}
