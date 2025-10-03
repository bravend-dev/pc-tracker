# check.ps1
# Run with PowerShell (Admin)
# PowerShell -ExecutionPolicy Bypass -File .\check.ps1

Write-Host "Scanning HTTPS connections (port 443)..." -ForegroundColor Cyan

# Get established connections to remote port 443
try {
    $connections = Get-NetTCPConnection -RemotePort 443 -State Established -ErrorAction Stop
} catch {
    Write-Host "Error: Unable to retrieve connection list. Please run with Administrator privileges." -ForegroundColor Red
    exit 1
}

if ($connections.Count -eq 0) {
    Write-Host "No active HTTPS connections found." -ForegroundColor Yellow
    exit 0
}

Write-Host "Found $($connections.Count) connection(s). Analyzing..." -ForegroundColor Green

$results = @()

foreach ($c in $connections) {
    $owningPid = $c.OwningProcess
    
    # Get process information
    try {
        $proc = Get-Process -Id $owningPid -ErrorAction Stop
        $procName = $proc.ProcessName
        $procPath = if ($proc.Path) { $proc.Path } else { "(unknown)" }
    } catch {
        $procName = "Unknown"
        $procPath = "(process not found)"
    }

    $ip = $c.RemoteAddress

    # Try reverse DNS (PTR)
    $ptr = "(none)"
    try {
        $dns = Resolve-DnsName -Name $ip -Type PTR -ErrorAction Stop -DnsOnly
        if ($dns) {
            $ptr = ($dns | Where-Object { $_.Type -eq 'PTR' } | Select-Object -First 1).NameHost
            if (-not $ptr) { $ptr = "(none)" }
        }
    } catch {
        # DNS lookup failed, keep default
    }

    # Try to obtain server certificate
    $certSubject = "(none)"
    $certIssuer = "(none)"
    
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient
        $connectTask = $tcp.BeginConnect($ip, 443, $null, $null)
        
        if ($connectTask.AsyncWaitHandle.WaitOne(2000)) {
            $tcp.EndConnect($connectTask)
            
            if ($tcp.Connected) {
                $stream = $tcp.GetStream()
                $ssl = New-Object System.Net.Security.SslStream(
                    $stream, 
                    $false,
                    ([System.Net.Security.RemoteCertificateValidationCallback]{ $true })
                )
                
                # Try authenticate with timeout
                $authTask = $ssl.BeginAuthenticateAsClient($ip, $null, $null)
                if ($authTask.AsyncWaitHandle.WaitOne(2000)) {
                    $ssl.EndAuthenticateAsClient($authTask)
                    
                    $remoteCert = $ssl.RemoteCertificate
                    if ($remoteCert) {
                        $x509 = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2 $remoteCert
                        $certSubject = $x509.Subject
                        $certIssuer = $x509.Issuer
                    }
                }
                
                $ssl.Close()
            }
        }
        
        $tcp.Close()
    } catch {
        # Ignore SSL/TLS handshake errors
    }

    $results += [PSCustomObject]@{
        ProcessName = $procName
        PID = $owningPid
        ProcessPath = $procPath
        LocalAddress = "$($c.LocalAddress):$($c.LocalPort)"
        RemoteIP = $ip
        RemotePort = $c.RemotePort
        ReverseDNS = $ptr
        CertSubject = $certSubject
        CertIssuer = $certIssuer
    }
}

# Display results
Write-Host "`nResults:" -ForegroundColor Cyan
$results | Format-Table ProcessName, PID, RemoteIP, ReverseDNS, CertSubject -AutoSize

# Export to file if needed
# $results | Export-Csv -Path "connections_report.csv" -NoTypeInformation -Encoding UTF8
# Write-Host "`nReport exported to: connections_report.csv" -ForegroundColor Green