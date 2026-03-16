rule Self_Deletion_Cleanup
{
    meta:
        description = "Self-deletion or cleanup behavior"
        severity = "medium"
        category = "stealth"

    strings:
        $s1 = "cmd.exe /c del"
        $s2 = "DeleteFile"
        $s3 = "RemoveDirectory"

    condition:
        any of them
}
