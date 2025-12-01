from fastapi import APIRouter
from ...service.meal import Neis
from ...utils.util import *
from base64 import b64decode
from pydantic import BaseModel
import json

meal = Neis()

router = APIRouter(prefix="/meal", tags=["meal"])

class mquery(BaseModel):
    code: str
    weekday: int = -1

@router.post("")
async def get_meal(query: mquery):
    allergy_map = {
        "1": "난류",
        "2": "우유",
        "3": "메밀",
        "4": "땅콩",
        "5": "대두",
        "6": "밀",
        "7": "고등어",
        "8": "게",
        "9": "새우",
        "10": "돼지고기",
        "11": "복숭아",
        "12": "토마토",
        "13": "아황산류",
        "14": "호두",
        "15": "닭고기",
        "16": "쇠고기",
        "17": "오징어",
        "18": "조개류(굴, 전복, 홍합 포함)",
        "19": "잣",
    }

    decoded = json.loads(b64decode(query.code).decode())
    m = await meal.get(
        decoded["n_region_code"], decoded["n_school_code"], get_weekdays(query.weekday)
    )
    diet = {}

    for i in m.DDISH_NM.split("<br/>"):
        i = i.rsplit(" ", 1)
        try:
            allergy = []
            i[1] = i[1].replace("(", "").replace(")", "")
            if i[1] != "":
                for z in i[1].split("."):
                    allergy.append(allergy_map[z])
            else:
                allergy = None
            diet[i[0]] = allergy

        except IndexError:
            diet[i[0]] = None
            continue

    origin = {}

    for i in m.ORPLC_INFO.split("<br/>"):
        i = i.split(" : ")
        origin[i[0]] = i[1]

    cal = m.CAL_INFO

    antelope = {}

    for i in m.NTR_INFO.split("<br/>"):
        i = i.split(" : ")
        antelope[i[0]] = i[1]

    return {"요리명": diet, "원산지": origin, "칼로리": cal, "영양성분": antelope}
