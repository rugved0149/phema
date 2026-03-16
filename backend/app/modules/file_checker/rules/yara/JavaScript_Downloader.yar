rule JavaScript_Downloader
{
    meta:
        description = "JavaScript downloading remote payload"
        severity = "high"
        category = "script"

    strings:
        $s1 = "XMLHttpRequest"
        $s2 = "ActiveXObject"
        $s3 = "ADODB.Stream"

    condition:
        2 of them
}
