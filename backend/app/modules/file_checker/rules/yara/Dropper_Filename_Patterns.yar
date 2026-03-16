rule Dropper_Filename_Patterns
{
    meta:
        description = "Common dropper filename patterns"
        severity = "low"
        category = "dropper"

    strings:
        $s1 = "update.exe"
        $s2 = "install.exe"
        $s3 = "setup.tmp"

    condition:
        any of them
}
