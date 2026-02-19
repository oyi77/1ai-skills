# XAUUSD Backtest Script (PowerShell Version)
# Period: 2025-01-01 to 2026-01-01
# Initial Balance: $100

param(
    [string]$Symbol = "GC=F",
    [double]$InitialBalance = 100.0,
    [string]$StartDate = "2025-01-01",
    [string]$EndDate = "2026-01-01",
    [int]$Lookback = 20,
    [double]$TpPct = 0.02,
    [double]$SlPct = 0.01
)

$ErrorActionPreference = "Stop"

function Write-Silent {
    param([string]$Message)
    Write-Host "[$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))] $Message"
}

function Download-Data {
    param([string]$Symbol, [string]$StartDate, [string]$EndDate)
    
    Write-Silent "Downloading $Symbol data from $StartDate to $EndDate..."
    
    # URL untuk Yahoo Finance historical data
    $startEpoch = [Math]::Floor((Get-Date $StartDate).ToUniversalTime().Subtract((Get-Date "1970-01-01")).TotalSeconds)
    $endEpoch = [Math]::Floor((Get-Date $EndDate).ToUniversalTime().Subtract((Get-Date "1970-01-01")).TotalSeconds)
    
    $url = "https://query1.finance.yahoo.com/v7/finance/download/$Symbol`?period1=$startEpoch`&period2=$endEpoch`&interval=1d`&events=history`&includeAdjustedClose=true"
    
    Write-Silent "URL: $url"
    
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing
        $csvContent = $response.Content
        
        if ($csvContent -match "404 Not Found" -or $csvContent -match "No data found") {
            Write-Silent "No data available for $Symbol"
            return $null
        }
        
        # Parse CSV
        $lines = $csvContent.Trim() -split "`n"
        $headers = ($lines[0] -split ",").Trim()
        
        $data = @()
        for ($i = 1; $i -lt $lines.Length; $i++) {
            $values = ($lines[$i] -split ",").Trim()
            if ($values.Length -ge 6) {
                $row = @{}
                for ($j = 0; $j -lt $headers.Length; $j++) {
                    $row[$headers[$j]] = $values[$j]
                }
                $data += [PSCustomObject]$row
            }
        }
        
        Write-Silent "Downloaded $($data.Count) bars"
        return $data
    }
    catch {
        Write-Silent "Error downloading data: $($_.Exception.Message)"
        return $null
    }
}

function Invoke-Backtest {
    param(
        [array]$Data,
        [double]$InitialBalance,
        [int]$Lookback,
        [double]$TpPct,
        [double]$SlPct
    )
    
    if ($Data.Count -eq 0) {
        return @()
    }
    
    $trades = @()
    $position = $null
    $entryPrice = 0
    $entryTime = $null
    
    $i = 0
    foreach ($row in $Data) {
        $high = [double]$row.High
        $low = [double]$row.Low
        $close = [double]$row.Close
        $date = $row.Date
        
        if ($i -lt $Lookback) {
            $i++
            continue
        }
        
        # Calculate lookback levels
        $lookbackHigh = ($Data | Select-Object -First $Lookback -Skip ($i - $Lookback) | Measure-Object -Property High -Maximum).Maximum
        $lookbackLow = ($Data | Select-Object -First $Lookback -Skip ($i - $Lookback) | Measure-Object -Property Low -Minimum).Minimum
        
        # Entry signals
        if ($null -eq $position) {
            if ($close -gt $lookbackHigh) {
                $position = 'long'
                $entryPrice = $close
                $entryTime = $date
                $trades += @{
                    Pair = "XAUUSD"
                    EntryTime = $date
                    ExitTime = $null
                    EntryPrice = $entryPrice
                    ExitPrice = $null
                    PnlUsd = $null
                    PnlPoints = $null
                    Win = $null
                }
            }
        }
        # Exit signals
        elseif ($position -eq 'long') {
            $exited = $false
            
            # TP hit
            if ($close -ge $entryPrice * (1 + $TpPct)) {
                $pnlPct = $TpPct
                $win = $true
                $exited = $true
            }
            # SL hit
            elseif ($close -le $entryPrice * (1 - $SlPct)) {
                $pnlPct = -$SlPct
                $win = $false
                $exited = $true
            }
            # Breakdown exit
            elseif ($close -lt $lookbackLow) {
                $pnlPct = ($close - $entryPrice) / $entryPrice
                $win = $pnlPct -gt 0
                $exited = $true
            }
            
            if ($exited) {
                $pnlUsd = [Math]::Round($InitialBalance * $pnlPct, 2)
                $pnlPoints = [Math]::Round(($close - $entryPrice) / 0.01, 2)
                
                $trades[-1].ExitTime = $date
                $trades[-1].ExitPrice = $close
                $trades[-1].PnlUsd = $pnlUsd
                $trades[-1].PnlPoints = $pnlPoints
                $trades[-1].Win = $win
                
                $position = $null
            }
        }
        
        $i++
    }
    
    # Close open position at end
    if ($null -ne $position -and $trades.Count -gt 0) {
        $lastClose = [double]($Data[-1].Close)
        $pnlPct = ($lastClose - $entryPrice) / $entryPrice
        $pnlUsd = [Math]::Round($InitialBalance * $pnlPct, 2)
        $pnlPoints = [Math]::Round(($lastClose - $entryPrice) / 0.01, 2)
        
        $trades[-1].ExitTime = $Data[-1].Date
        $trades[-1].ExitPrice = $lastClose
        $trades[-1].PnlUsd = $pnlUsd
        $trades[-1].PnlPoints = $pnlPoints
        $trades[-1].Win = $pnlUsd -gt 0
    }
    
    return $trades
}

function Invoke-Analyze {
    param([array]$Trades, [double]$InitialBalance)
    
    if ($Trades.Count -eq 0) {
        return $null
    }
    
    $totalTrades = $Trades.Count
    $winCount = ($Trades | Where-Object { $_.Win }).Count
    $lossCount = $totalTrades - $winCount
    
    $pnlUsdList = $Trades | Where-Object { $null -ne $_.PnlUsd } | ForEach-Object { $_.PnlUsd }
    $pnlPointsList = $Trades | Where-Object { $null -ne $_.PnlPoints } | ForEach-Object { $_.PnlPoints }
    
    $grossProfit = ($pnlUsdList | Where-Object { $_ -gt 0 } | Measure-Object -Sum).Sum
    $grossLoss = ($pnlUsdList | Where-Object { $_ -lt 0 } | Measure-Object -Sum).Sum
    $netPnl = ($pnlUsdList | Measure-Object -Sum).Sum
    
    $wins = $pnlUsdList | Where-Object { $_ -gt 0 }
    $losses = $pnlUsdList | Where-Object { $_ -lt 0 }
    
    $avgWin = if ($wins.Count -gt 0) { [Math]::Round($grossProfit / $wins.Count, 2) } else { 0 }
    $avgLoss = if ($losses.Count -gt 0) { [Math]::Round([Math]::Abs($grossLoss) / $losses.Count, 2) } else { 0 }
    
    $profitFactor = if ($grossLoss -ne 0) { [Math]::Round($grossProfit / [Math]::Abs($grossLoss), 2) } else { if ($grossProfit -gt 0) { 999 } else { 0 } }
    
    # Calculate drawdown
    $equity = $InitialBalance
    $peak = $InitialBalance
    $maxDrawdown = 0
    
    foreach ($pnl in $pnlUsdList) {
        $equity += $pnl
        if ($equity -gt $peak) {
            $peak = $equity
        }
        $drawdown = $peak - $equity
        if ($drawdown -gt $maxDrawdown) {
            $maxDrawdown = $drawdown
        }
    }
    
    $endingBalance = $InitialBalance + $netPnl
    $returnPct = if ($InitialBalance -gt 0) { [Math]::Round(($endingBalance - $InitialBalance) / $InitialBalance * 100, 2) } else { 0 }
    $maxDrawdownPct = if ($peak -gt 0) { [Math]::Round($maxDrawdown / $peak * 100, 2) } else { 0 }
    
    return @{
        TotalTrades = $totalTrades
        WinCount = $winCount
        LossCount = $lossCount
        WinRate = if ($totalTrades -gt 0) { [Math]::Round($winCount / $totalTrades * 100, 2) } else { 0 }
        GrossProfit = [Math]::Round($grossProfit, 2)
        GrossLoss = [Math]::Round([Math]::Abs($grossLoss), 2)
        NetPnl = [Math]::Round($netPnl, 2)
        AvgWin = $avgWin
        AvgLoss = -$avgLoss
        ProfitFactor = $profitFactor
        MaxDrawdown = [Math]::Round($maxDrawdown, 2)
        MaxDrawdownPct = $maxDrawdownPct
        InitialBalance = $InitialBalance
        EndingBalance = [Math]::Round($endingBalance, 2)
        ReturnPct = $returnPct
        Pairs = @("XAUUSD")
    }
}

function Write-Summary {
    param([hashtable]$Metrics)
    
    if ($null -eq $Metrics) {
        Write-Host "No trades to summarize!"
        return
    }
    
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host ("{0,-60}" -f "  XAUUSD BACKTEST SUMMARY") -ForegroundColor Cyan
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host "PERIOD            : 2025-01-01 to 2026-01-01"
    Write-Host "STRATEGY          : Breakout (lookback=20, TP=2%, SL=1%)"
    Write-Host ("-" * 60)
    Write-Host "PAIR              : $($Metrics.Pairs[0])"
    Write-Host "Total Trades      : $($Metrics.TotalTrades)"
    Write-Host "Win Rate          : $($Metrics.WinRate)%"
    Write-Host ("-" * 60)
    Write-Host "BALANCE"
    Write-Host ("  Initial Balance : {0:N2}" -f $Metrics.InitialBalance)
    Write-Host ("  Ending Balance  : {0:N2}" -f $Metrics.EndingBalance)
    Write-Host ("  Net PNL         : {0:N2} ({1:N2}%%)" -f $Metrics.NetPnl, $Metrics.ReturnPct)
    Write-Host ("-" * 60)
    Write-Host "DRAWDOWN"
    Write-Host ("  Max Drawdown    : {0:N2} ({1:N2}%%)" -f $Metrics.MaxDrawdown, $Metrics.MaxDrawdownPct)
    Write-Host ("-" * 60)
    Write-Host "PNL (USD)"
    Write-Host ("  Gross Profit    : {0:N2}" -f $Metrics.GrossProfit)
    Write-Host ("  Gross Loss      : {0:N2}" -f $Metrics.GrossLoss)
    Write-Host ("  Avg Win         : {0:N2}" -f $Metrics.AvgWin)
    Write-Host ("  Avg Loss        : {0:N2}" -f $Metrics.AvgLoss)
    Write-Host ("-" * 60)
    Write-Host ("PROFIT FACTOR     : {0:N2}" -f $Metrics.ProfitFactor)
    Write-Host ("=" * 60) -ForegroundColor Cyan
}

# Main execution
Write-Host ""
Write-Host "XAUUSD Backtest" -ForegroundColor Green
Write-Host "Period: 2025-01-01 to 2026-01-01"
Write-Host "Initial Balance: `$$InitialBalance"
Write-Host ""

# Download data
$Data = Download-Data -Symbol $Symbol -StartDate $StartDate -EndDate $EndDate

if ($null -eq $Data -or $Data.Count -eq 0) {
    Write-Host "Failed to download data!" -ForegroundColor Red
    exit 1
}

$firstDate = $Data[0].Date
$lastDate = $Data[-1].Date
$closePrices = $Data | ForEach-Object { [double]$_.Close }
$minPrice = ($closePrices | Measure-Object -Minimum).Minimum
$maxPrice = ($closePrices | Measure-Object -Maximum).Maximum

Write-Host ""
Write-Host "Data range: $firstDate to $lastDate"
Write-Host "Price range: `$$minPrice - `$$maxPrice"

# Run backtest
Write-Host ""
Write-Host "Running breakout strategy backtest..." -ForegroundColor Yellow

$Trades = Invoke-Backtest -Data $Data -InitialBalance $InitialBalance -Lookback $Lookback -TpPct $TpPct -SlPct $SlPct

if ($Trades.Count -eq 0) {
    Write-Host "No trades generated!" -ForegroundColor Yellow
    exit 0
}

Write-Host "Generated $($Trades.Count) trades"

# Analyze results
$Metrics = Invoke-Analyze -Trades $Trades -InitialBalance $InitialBalance

# Print summary
Write-Summary -Metrics $Metrics
