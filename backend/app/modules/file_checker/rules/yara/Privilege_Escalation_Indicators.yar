rule Privilege_Escalation_Indicators
{
    meta:
        description = "Privilege escalation related artifacts"
        severity = "high"
        category = "privilege"

    strings:
        $s1 = "SeDebugPrivilege"
        $s2 = "runas"
        $s3 = "TokenElevation"

    condition:
        any of them
}
