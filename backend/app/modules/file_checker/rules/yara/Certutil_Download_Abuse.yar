rule Certutil_Download_Abuse
{
    meta:
        description = "Certutil used to download or decode payload"
        severity = "high"
        category = "lolbin"

    strings:
        $s1 = "certutil -urlcache"
        $s2 = "certutil -decode"

    condition:
        any of them
}
