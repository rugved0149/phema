rule Self_Deletion_Cleanup
{
meta:
description = "Self deletion artifacts"
severity = "medium"
category = "stealth"

strings:
$s1 = "cmd.exe /c del"
$s2 = "DeleteFile"
$s3 = "RemoveDirectory"

condition:
uint16(0) == 0x5A4D and 2 of them
}