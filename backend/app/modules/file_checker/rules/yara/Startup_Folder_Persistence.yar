rule Startup_Folder_Persistence
{
    meta:
        description = "Startup folder persistence"
        severity = "medium"
        category = "persistence"

    strings:
        $s1 = "\\Start Menu\\Programs\\Startup"

    condition:
        $s1
}
