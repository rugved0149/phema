rule Privilege_Escalation_Indicators
{
meta:
description = "Privilege escalation indicators"
severity = "high"
category = "privilege"

strings:
$s1 = "SeDebugPrivilege"
$s2 = "runas"
$s3 = "TokenElevation"

condition:
uint16(0) == 0x5A4D and 2 of them
}
