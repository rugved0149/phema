rule Keylogging_Functions
{
    meta:
        description = "Keyboard input capture indicators"
        severity = "high"
        category = "surveillance"

    strings:
        $s1 = "GetAsyncKeyState"
        $s2 = "SetWindowsHookEx"
        $s3 = "WH_KEYBOARD_LL"

    condition:
        any of them
}
