# check-post-approx.ps1
$intervalSec = 60

Write-Host "Starting approximate POST-frequency watcher (by counting outbound connections to :80/:443). Ctrl+C to stop."
while ($true) {
    $start = Get-Date
    # collect snapshot of outbound TCP connections
    $conns = Get-NetTCPConnection -State Established |
        Where-Object { $_.RemotePort -in 80, 443 -and $_.RemoteAddress -ne '127.0.0.1' -and $_.RemoteAddress -ne '::1' }

    # join with process names (try-catch because some PIDs may disappear)
    $rows = foreach ($c in $conns) {
        $procName = $null
        try {
            $proc = Get-Process -Id $c.OwningProcess -ErrorAction Stop
            $procName = $proc.ProcessName
        } catch {
            $procName = "PID_$($c.OwningProcess)"
        }
        [PSCustomObject]@{
            Time = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
            Process = $procName
            PID = $c.OwningProcess
            Remote = "$($c.RemoteAddress):$($c.RemotePort)"
        }
    }

    # group and print counts
    $rows | Group-Object Process, PID | Sort-Object Count -Descending |
        Select-Object @{Name='Count';Expression={$_.Count}}, @{Name='Process';Expression={$_.Name}} |
        Format-Table -AutoSize

    # sleep until next interval (account for time spent)
    $elapsed = (Get-Date) - $start
    $sleep = $intervalSec - [math]::Max(0, [int]$elapsed.TotalSeconds)
    Start-Sleep -Seconds $sleep
}
