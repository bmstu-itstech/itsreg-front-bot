from apscheduler.schedulers.asyncio import AsyncIOScheduler


job_defaults = {
    "max_instances": 10000
}


scheduler = AsyncIOScheduler(job_defaults=job_defaults)