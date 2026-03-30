rule High_Base64_Usage
{
meta:
description = "Suspicious heavy Base64 usage in executable"
severity = "medium"
category = "obfuscation"

strings:
$b64 = /[A-Za-z0-9+\/]{120,}={0,2}/

condition:
uint16(0) == 0x5A4D and #b64 > 5
}