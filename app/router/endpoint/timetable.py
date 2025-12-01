from fastapi import APIRouter
from base64 import b64decode
from pydantic import BaseModel
import json
from ...service.timetable import Comci
from ...utils.util import *

tt = Comci()

router = APIRouter(prefix="/timetable", tags=["timetable"])


class ttquery(BaseModel):
    code: str
    grade: int
    class_: int
    weekday: int = -1


@router.post("")
async def get_timetable(query: ttquery):
    decoded = json.loads(b64decode(query.code).decode())
    return tt.get(
        decoded["c_school"],
        decoded["c_region_code"],
        decoded["c_school_code"],
        query.grade,
        query.class_,
        get_weekdays(query.weekday),
    )
