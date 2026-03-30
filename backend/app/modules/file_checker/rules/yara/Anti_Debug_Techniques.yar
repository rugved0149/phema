rule Anti_Debug_Techniques
{
meta:
description = "Anti-debugging technique indicators"
severity = "medium"
category = "anti-analysis"

strings:
$s1 = "IsDebuggerPresent"
$s2 = "CheckRemoteDebuggerPresent"
$s3 = "NtQueryInformationProcess"

condition:
uint16(0) == 0x5A4D and 2 of them
}