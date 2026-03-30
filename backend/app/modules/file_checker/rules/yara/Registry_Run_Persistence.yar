rule Registry_Run_Persistence
{
meta:
description = "Registry persistence indicators"
severity = "medium"
category = "persistence"

strings:
$reg1 = "CurrentVersion\\Run"
$reg2 = "CurrentVersion\\RunOnce"

condition:
uint16(0) == 0x5A4D and any of them
}