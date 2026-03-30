rule Keylogging_Functions
{
meta:
description = "Keyboard capture APIs"
severity = "high"
category = "surveillance"

strings:
$s1 = "GetAsyncKeyState"
$s2 = "SetWindowsHookEx"
$s3 = "WH_KEYBOARD_LL"

condition:
uint16(0) == 0x5A4D and 2 of them
}
