rule Hardcoded_C2_Indicators
{
    meta:
        description = "Hardcoded IP or suspicious domain"
        severity = "medium"
        category = "network"

    strings:
        $ip = /\b\d{1,3}(\.\d{1,3}){3}\b/
        $tld = ".ru"
        $tld2 = ".xyz"

    condition:
        any of them
}
