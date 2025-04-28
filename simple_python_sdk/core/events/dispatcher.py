import asyncio
from typing import Any, Callable, Dict

from simple_python_sdk.core.events.store import RedisEventStore


class EventDispatcher:
    def __init__(self,redis_url: str):
        self.hanlers: Dict[str,list[Callable]] = {}
        self.store = RedisEventStore(redis_url)
        
    def register_handler(self,event_type: str,handler: Callable):
        if event_type not in self.hanlers:
            self.hanlers[event_type] = []
        self.hanlers[event_type].append(handler)
    async def dispatch(self,event_type: str,payload: Dict[str,Any]):
        await self.store.store_event(event_type,payload)

        if event_type in self.hanlers:
            await asyncio.gather(
                *[handler(payload) for handler in self.hanlers[event_type]]
            )
