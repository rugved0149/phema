rule Scheduled_Task_Persistence
{
    meta:
        description = "Scheduled task based persistence"
        severity = "medium"
        category = "persistence"

    strings:
        $s1 = "schtasks"
        $s2 = "/create"
        $s3 = "Task Scheduler"

    condition:
        any of them
}
