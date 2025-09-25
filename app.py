from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class Event(BaseModel):
    device_id: str
    presence: int
    movement: int
    moving_range: int
    fall_state: int
    dwell_state: int
    ts: int

@app.post("/events")
async def receive_event(ev: Event):
    print({"time": datetime.now().isoformat(), **ev.dict()})
    return {"ok": True}
