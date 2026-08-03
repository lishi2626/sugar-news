param(
    [string]$TaskName = "SugarNewsDailyUpdate",
    [string]$At = "06:40",
    [string]$VercelBaseUrl = "https://sugar-news.vercel.app"
)

$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$dailyScript = Join-Path $projectRoot "scripts\Run-Sugar-News.ps1"
$powershell = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
$taskArguments = "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$dailyScript`" -VercelBaseUrl `"$VercelBaseUrl`" -SkipIfSuccess"
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

$action = New-ScheduledTaskAction `
    -Execute $powershell `
    -Argument $taskArguments `
    -WorkingDirectory $projectRoot

$trigger = New-ScheduledTaskTrigger -Daily -At $At
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)
$principal = New-ScheduledTaskPrincipal `
    -UserId $currentUser `
    -LogonType S4U `
    -RunLevel Limited

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Refresh Sugar News at $At Asia/Shanghai, publish updates, and verify the Vercel production page." `
    -Force | Out-Null

$task = Get-ScheduledTask -TaskName $TaskName
$info = Get-ScheduledTaskInfo -TaskName $TaskName

[pscustomobject]@{
    TaskName = $task.TaskName
    State = $task.State
    NextRunTime = $info.NextRunTime
    Script = $dailyScript
    WorkingDirectory = $projectRoot
    VercelBaseUrl = $VercelBaseUrl
}
