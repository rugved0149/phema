rule UPX_Packed_Executable
{
    meta:
        description = "Executable packed with UPX"
        severity = "medium"
        category = "packer"

    strings:
        $s1 = "UPX0"
        $s2 = "UPX1"
        $s3 = "UPX!"

    condition:
        any of them
}
