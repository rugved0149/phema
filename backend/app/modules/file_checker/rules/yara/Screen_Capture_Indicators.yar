rule Screen_Capture_Indicators
{
    meta:
        description = "Screen capture related APIs"
        severity = "medium"
        category = "surveillance"

    strings:
        $s1 = "BitBlt"
        $s2 = "GetDC"
        $s3 = "CreateCompatibleBitmap"

    condition:
        2 of them
}
