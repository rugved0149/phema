rule Suspicious_PowerShell_Execution
{
    meta:
        description = "PowerShell used with execution-bypass flags"
        severity = "high"
        category = "execution"

    strings:
        $ps1 = "powershell -nop"
        $ps2 = "powershell -noni"
        $ps3 = "ExecutionPolicy Bypass"

    condition:
        any of them
}
