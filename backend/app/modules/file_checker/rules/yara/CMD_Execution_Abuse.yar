rule CMD_Execution_Abuse
{
    meta:
        description = "Windows command shell execution"
        severity = "medium"
        category = "execution"

    strings:
        $cmd1 = "cmd.exe /c"
        $cmd2 = "cmd /c"

    condition:
        any of them
}
