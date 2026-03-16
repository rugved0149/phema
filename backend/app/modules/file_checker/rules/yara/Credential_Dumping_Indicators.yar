rule Credential_Dumping_Indicators
{
    meta:
        description = "Indicators of credential dumping"
        severity = "high"
        category = "credential-access"

    strings:
        $s1 = "LSASS"
        $s2 = "sekurlsa"
        $s3 = "logonpasswords"

    condition:
        any of them
}
