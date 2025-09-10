from fastapi import FastAPI
from pytz import timezone
from datetime import datetime, timedelta
from base64 import b64encode, b64decode
import json

from timetable import Comci

from meal import Neis

meal = Neis()
tt = Comci()


def get_seoul_time():
    seoul_tz = timezone("Asia/Seoul")
    return datetime.now(seoul_tz)


app = FastAPI(
    title="Classfood Timetable API",
    description="학교 급식 및 시간표 API",
    version="0.0.1",
)


@app.get("/timetable/get")
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


@app.get("/search")
async def search_timetable(school_name_comci: str, school_name_neis: str = None): # type: ignore
    if school_name_neis is None:
        school_name_neis = school_name_comci

    com = tt.search_school(school_name_comci)
    nei = await meal.search_school(school_name_neis)
    if len(nei) > 1:
        return "검색범위를 좁혀주세요"
    nei = nei[0]
    if len(com) > 1:
        return "검색범위를 좁혀주세요"
    com = com[0]

    ret = {"comci_region": com[1], "comci_school": com[2], "neis_school": nei.SCHUL_NM, "neis_region": nei.ATPT_OFCDC_SC_NM}
    ret["code"] = b64encode(
        json.dumps(
            {
                "n_region_code": nei.ATPT_OFCDC_SC_CODE,
                "n_school_code": nei.SD_SCHUL_CODE,
                "c_region_code": com[0],
                "c_region": com[1],
                "c_school": com[2],
                "c_school_code": com[3],
            },
            ensure_ascii=False,
        ).encode()
    ).decode()
    return ret


@app.get("/meal")
async def get_meal(code):
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
        "19": "잣"
    }

    decoded = json.loads(b64decode(code).decode())
    m = await meal.get(
        decoded["n_region_code"],
        decoded["n_school_code"],
        get_seoul_time()
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
