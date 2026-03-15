# states/timeout_tasks.py
import asyncio

timeout_tasks: dict[tuple[int, int], asyncio.Task] = {}
