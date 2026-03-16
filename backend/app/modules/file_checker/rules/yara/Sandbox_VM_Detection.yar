rule Sandbox_VM_Detection
{
    meta:
        description = "Detects sandbox or VM detection techniques"
        severity = "high"
        category = "anti-analysis"

    strings:
        $s1 = "vboxservice"
        $s2 = "vmtoolsd"
        $s3 = "VirtualBox"
        $s4 = "VMware"

    condition:
        any of them
}
