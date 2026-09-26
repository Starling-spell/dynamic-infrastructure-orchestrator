param([Parameter(Mandatory=$true)][string]$Address,
      [Parameter(Mandatory=$true)][string]$FixtureCommit,
      [Parameter(Mandatory=$true)][string]$CliEntry)
$base = "https://raw.githubusercontent.com/Starling-spell/dynamic-infrastructure-orchestrator/$FixtureCommit/examples"
$spec = (Get-FileHash -Algorithm SHA256 -LiteralPath "$PSScriptRoot/../examples/specification.txt").Hash.ToLower()
$runbook = (Get-FileHash -Algorithm SHA256 -LiteralPath "$PSScriptRoot/../examples/runbook.txt").Hash.ToLower()
& node $CliEntry network set studionet
& node $CliEntry write $Address create_network --args cooling-demo "$base/specification.txt" $spec "$base/runbook.txt" $runbook
& node $CliEntry write $Address register_component --args cooling-demo cooling ACTIVE
& node $CliEntry write $Address register_component --args cooling-demo machine ACTIVE cooling
& node $CliEntry write $Address seal_network --args cooling-demo
$deadline = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds() + 3600
$steps = 'machine|ACTIVE|STANDBY;cooling|ACTIVE|MAINTENANCE'
& node $CliEntry write $Address propose_transition_compact --args cooling-demo safe-maintenance 0 $steps $deadline
& node $CliEntry write $Address apply_transition --args cooling-demo safe-maintenance
& node $CliEntry call $Address get_plan --args cooling-demo safe-maintenance
& node $CliEntry call $Address get_record --args cooling-demo safe-maintenance
& node $CliEntry call $Address get_network --args cooling-demo
