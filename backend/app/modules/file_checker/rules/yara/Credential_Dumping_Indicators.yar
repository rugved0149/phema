rule Credential_Dumping_Indicators
{
meta:
description = "Credential dumping artifacts"
severity = "high"
category = "credential-access"

strings:
$s1 = "LSASS"
$s2 = "sekurlsa"
$s3 = "logonpasswords"

condition:
uint16(0) == 0x5A4D and 2 of them
}
