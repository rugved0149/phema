rule Encoded_PowerShell_Command
{
    meta:
        description = "Base64 encoded PowerShell command"
        severity = "high"
        category = "obfuscation"

    strings:
        $enc = "-EncodedCommand"
        $b64 = /[A-Za-z0-9+\/]{40,}={0,2}/

    condition:
        $enc and $b64
}
