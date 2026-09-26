param([Parameter(Mandatory=$true)][string]$Address,
      [Parameter(Mandatory=$true)][string]$FixtureCommit)
$base = "https://raw.githubusercontent.com/Starling-spell/dynamic-infrastructure-orchestrator/$FixtureCommit/examples"
$spec = (Get-FileHash -Algorithm SHA256 -LiteralPath "$PSScriptRoot/../examples/specification.txt").Hash.ToLower()
$runbook = (Get-FileHash -Algorithm SHA256 -LiteralPath "$PSScriptRoot/../examples/runbook.txt").Hash.ToLower()
genlayer network set studionet
genlayer write $Address create_network --args cooling-demo "$base/specification.txt" $spec "$base/runbook.txt" $runbook
genlayer write $Address register_component --args cooling-demo cooling ACTIVE
genlayer write $Address register_component --args cooling-demo machine ACTIVE cooling
genlayer write $Address seal_network --args cooling-demo
$deadline = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds() + 3600
$steps = '[{"component":"machine","from":"ACTIVE","to":"STANDBY"},{"component":"cooling","from":"ACTIVE","to":"MAINTENANCE"}]'
genlayer write $Address propose_transition --args cooling-demo safe-maintenance 0 $steps $deadline
genlayer write $Address apply_transition --args cooling-demo safe-maintenance
genlayer call $Address get_plan --args cooling-demo safe-maintenance
genlayer call $Address get_record --args cooling-demo safe-maintenance
genlayer call $Address get_network --args cooling-demo
