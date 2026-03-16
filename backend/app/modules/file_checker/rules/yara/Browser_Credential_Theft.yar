rule Browser_Credential_Theft
{
    meta:
        description = "Browser credential access indicators"
        severity = "high"
        category = "credential-access"

    strings:
        $s1 = "Login Data"
        $s2 = "Cookies"
        $s3 = "Web Data"

    condition:
        all of them
}
