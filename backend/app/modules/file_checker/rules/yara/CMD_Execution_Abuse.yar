rule CMD_Execution_Abuse
{
meta:
description = "Command shell execution pattern"
severity = "medium"
category = "execution"

strings:
$cmd1 = "cmd.exe /c"
$cmd2 = "cmd /c"

condition:
uint16(0) == 0x5A4D and all of them
}
