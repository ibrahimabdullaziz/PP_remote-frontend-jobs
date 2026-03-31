import aiosqlite
from config.settings import DATABASE_PATH
import os

async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS processed_jobs (
                job_id TEXT PRIMARY KEY,
                platform TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def is_job_processed(job_id: str) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT 1 FROM processed_jobs WHERE job_id = ?', (job_id,)) as cursor:
            return await cursor.fetchone() is not None

async def mark_job_processed(job_id: str, platform: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            'INSERT OR IGNORE INTO processed_jobs (job_id, platform) VALUES (?, ?)',
            (job_id, platform)
        )
        await db.commit()
