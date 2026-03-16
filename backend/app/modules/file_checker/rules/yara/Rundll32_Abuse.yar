rule Rundll32_Abuse
{
    meta:
        description = "Suspicious rundll32 execution"
        severity = "medium"
        category = "lolbin"

    strings:
        $s1 = "rundll32"
        $s2 = ".dll,"

    condition:
        all of them
}
