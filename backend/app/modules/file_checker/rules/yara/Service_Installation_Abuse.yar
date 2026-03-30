rule Service_Installation_Abuse
{
meta:
description = "Service persistence creation"
severity = "medium"
category = "persistence"

strings:
$s1 = "CreateService"
$s2 = "StartService"
$s3 = "SERVICE_AUTO_START"

condition:
uint16(0) == 0x5A4D and 2 of them
}
