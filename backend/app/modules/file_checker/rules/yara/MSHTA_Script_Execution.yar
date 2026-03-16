rule MSHTA_Script_Execution
{
    meta:
        description = "MSHTA used to execute scripts"
        severity = "high"
        category = "lolbin"

    strings:
        $s1 = "mshta.exe"
        $s2 = "javascript:"
        $s3 = "vbscript:"

    condition:
        $s1 and any of ($s2, $s3)
}
