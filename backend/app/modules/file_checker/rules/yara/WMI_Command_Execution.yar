rule WMI_Command_Execution
{
    meta:
        description = "WMI used for command execution"
        severity = "high"
        category = "execution"

    strings:
        $s1 = "wmic process call create"
        $s2 = "Win32_Process"

    condition:
        any of them
}
