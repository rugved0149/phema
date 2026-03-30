rule Scheduled_Task_Persistence
{
meta:
description = "Scheduled task persistence"
severity = "medium"
category = "persistence"

strings:
$s1 = "schtasks"
$s2 = "/create"
$s3 = "Task Scheduler"

condition:
uint16(0) == 0x5A4D and 2 of them
}
