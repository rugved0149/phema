rule Executable_Inside_Archive
{
meta:
description = "Executable embedded in ZIP archive"
severity = "medium"
category = "archive"

strings:
$s1 = ".exe"
$s2 = ".scr"

condition:
uint16(0) == 0x504B and 2 of them
}
