rule Anti_Debug_Techniques
{
    meta:
        description = "Common anti-debugging techniques"
        severity = "high"
        category = "anti-analysis"

    strings:
        $s1 = "IsDebuggerPresent"
        $s2 = "CheckRemoteDebuggerPresent"
        $s3 = "NtQueryInformationProcess"

    condition:
        any of them
}
