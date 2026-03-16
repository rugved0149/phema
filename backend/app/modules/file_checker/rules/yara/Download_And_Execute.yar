rule Download_And_Execute
{
    meta:
        description = "Downloads payload and executes it"
        severity = "high"
        category = "loader"

    strings:
        $url1 = "http://"
        $url2 = "https://"
        $exec1 = "Invoke-WebRequest"
        $exec2 = "curl "
        $exec3 = "wget "

    condition:
        (any of ($exec*)) and (any of ($url*))
}