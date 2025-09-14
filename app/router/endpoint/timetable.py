from fastapi import APIRouter
from base64 import b64decode
import json
from ...service.timetable import Comci
from ...utils.util import * 
tt = Comci()

router = APIRouter(prefix="/timetable", tags=["timetable"])

@router.get("/")
async def get_timetable(code: str, grade: int, class_: int):
    decoded = json.loads(b64decode(code).decode())
    return tt.get(
        decoded["c_school"],
        decoded["c_region_code"],
        decoded["c_school_code"],
        grade,
        class_,
        get_seoul_time(),
    )
