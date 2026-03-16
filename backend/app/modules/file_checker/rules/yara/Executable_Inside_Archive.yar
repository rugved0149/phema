rule Executable_Inside_Archive
{
    meta:
        description = "Executable embedded in archive"
        severity = "medium"
        category = "archive"

    strings:
        $s1 = ".exe"
        $s2 = ".scr"

    condition:
        filesize < 10MB and any of them
}
