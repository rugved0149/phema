rule Sandbox_VM_Detection
{
meta:
description = "VM detection indicators"
severity = "medium"
category = "anti-analysis"

strings:
$s1 = "vboxservice"
$s2 = "vmtoolsd"
$s3 = "VirtualBox"
$s4 = "VMware"

condition:
uint16(0) == 0x5A4D and 2 of them
}
