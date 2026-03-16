rule Registry_Run_Persistence
{
    meta:
        description = "Registry-based persistence mechanism"
        severity = "medium"
        category = "persistence"

    strings:
        $reg1 = "CurrentVersion\\Run"
        $reg2 = "CurrentVersion\\RunOnce"

    condition:
        any of them
}
