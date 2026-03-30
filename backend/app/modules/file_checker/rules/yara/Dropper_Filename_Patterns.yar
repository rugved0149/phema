rule Dropper_Filename_Patterns
{
meta:
description = "Common dropper filenames"
severity = "low"
category = "dropper"

strings:
$s1 = "update.exe"
$s2 = "install.exe"
$s3 = "setup.tmp"

condition:
uint16(0) == 0x5A4D and any of them
}
