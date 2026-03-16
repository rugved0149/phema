rule Executable_Masquerading
{
    meta:
        description = "Executable disguised as document"
        severity = "high"
        category = "masquerade"

    condition:
        uint16(0) == 0x5A4D and filesize < 2MB
}
