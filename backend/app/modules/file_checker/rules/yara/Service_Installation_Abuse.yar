rule Service_Installation_Abuse
{
    meta:
        description = "Service creation for persistence"
        severity = "medium"
        category = "persistence"

    strings:
        $s1 = "CreateService"
        $s2 = "StartService"
        $s3 = "SERVICE_AUTO_START"

    condition:
        any of them
}
