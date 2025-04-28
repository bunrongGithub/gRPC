
import json
import time
from typing import Any, Dict
import redis
class RedisEventStore:
    def __init__(self,redis_url: str,stream_name: str = "sdk_events"):
        self.redis=redis.Redis.from_url(redis_url)
        self.stream_name=stream_name
    async def store_event(self,event_type: str,payload: Dict[str,Any]):
        """Store any event in Redis stream"""
        event_data = {
            "type": event_type,
            "payload":json.dumps(payload),
            "timestamp":int(time.time() * 1000)
        }
        if event_data:
            print(event_data)
        return self.redis.xadd(self.stream_name,event_data)
    async def get_events(self,count: int = 100):
        raw_event = self.redis.xrevrange(self.stream_name,count=count)
        events = []
        for event_id,event_data in raw_event:
             parsed_data = {
            "id": event_id.decode(),  # Redis returns bytes
            "type": event_data.get(b"type", b"").decode(),
            "payload": json.loads(event_data.get(b"payload", b"{}").decode()),
            "timestamp": int(event_data.get(b"timestamp", b"0").decode())
        }
        events.append(parsed_data)
        return events