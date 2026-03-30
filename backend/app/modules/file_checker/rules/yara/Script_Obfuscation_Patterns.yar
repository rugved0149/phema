rule Script_Obfuscation_Patterns
{
meta:
description = "Script obfuscation indicators"
severity = "medium"
category = "obfuscation"

strings:
$s1 = "eval("
$s2 = "fromCharCode"
$s3 = "WScript.Shell"

condition:
uint16(0) == 0x5A4D and 2 of them
}
