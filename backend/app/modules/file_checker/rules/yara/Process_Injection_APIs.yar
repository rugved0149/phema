rule Process_Injection_APIs
{
    meta:
        description = "Common Windows process injection APIs"
        severity = "high"
        category = "injection"

    strings:
        $api1 = "VirtualAllocEx"
        $api2 = "WriteProcessMemory"
        $api3 = "CreateRemoteThread"

    condition:
        2 of them
}
