# watch-new-flows.ps1
param([int]$IntervalSec = 60)

$seen = @{}  # key => firstSeen timestamp

Write-Host "Watching NEW outbound TCP flows to :80/:443 (approx POST frequency). Ctrl+C to stop."

while ($true) {
    $loopStart = Get-Date

    $conns = Get-NetTCPConnection -State Established, SynSent, SynReceived |
        Where-Object { $_.RemotePort -in 80,443 -and $_.RemoteAddress -notin @('127.0.0.1','::1') }

    $nowKeys = @{}
    $newRows = foreach ($c in $conns) {
        $key = '{0}:{1}->{2}:{3}#{4}' -f $c.LocalAddress,$c.LocalPort,$c.RemoteAddress,$c.RemotePort,$c.OwningProcess
        $nowKeys[$key] = $true
        if (-not $seen.ContainsKey($key)) {
            $seen[$key] = (Get-Date)
            try { $procName = (Get-Process -Id $c.OwningProcess -ErrorAction Stop).ProcessName }
            catch { $procName = "PID_$($c.OwningProcess)" }
            [PSCustomObject]@{
                Time    = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
                Process = $procName
                PID     = $c.OwningProcess
                Remote  = "$($c.RemoteAddress):$($c.RemotePort)"
            }
        }
    }

    # dọn dẹp flow đã đóng để không phình bộ nhớ
    foreach ($k in @($seen.Keys)) { if (-not $nowKeys.ContainsKey($k)) { $null = $seen.Remove($k) } }

    Clear-Host
    Write-Host "New outbound TCP flows in the last interval:"
    if ($newRows) {
        $newRows | Group-Object Process, PID | Sort-Object Count -Descending |
            Select-Object @{n='NewConns';e={$_.Count}},
                          @{n='Process';e={$_.Group[0].Process}},
                          @{n='PID';e={$_.Group[0].PID}} |
            Format-Table -AutoSize
    } else {
        Write-Host "(no new TCP flows to :80/:443)"
    }

    $elapsed = [int]((Get-Date) - $loopStart).TotalSeconds
    Start-Sleep -Seconds ([Math]::Max(0, $IntervalSec - $elapsed))
}
