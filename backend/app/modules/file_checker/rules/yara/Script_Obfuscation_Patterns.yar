rule Script_Obfuscation_Patterns
{
    meta:
        description = "Obfuscated script constructs"
        severity = "high"
        category = "obfuscation"

    strings:
        $s1 = "eval("
        $s2 = "fromCharCode"
        $s3 = "WScript.Shell"

    condition:
        any of them
}
