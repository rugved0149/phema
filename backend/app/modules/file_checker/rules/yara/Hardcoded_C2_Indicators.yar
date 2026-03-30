rule Hardcoded_C2_Indicators
{
meta:
description = "Hardcoded C2 indicators"
severity = "medium"
category = "network"

strings:
$ip = /\b\d{1,3}(\.\d{1,3}){3}\b/
$tld1 = ".ru"
$tld2 = ".xyz"

condition:
uint16(0) == 0x5A4D and $ip and any of ($tld*)
}
