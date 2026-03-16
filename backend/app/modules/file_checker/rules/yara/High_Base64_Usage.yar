rule High_Base64_Usage
{
    meta:
        description = "Suspicious heavy Base64 usage"
        severity = "medium"
        category = "obfuscation"

    strings:
        $b64 = /[A-Za-z0-9+\/]{80,}={0,2}/

    condition:
        #b64 > 2
}
