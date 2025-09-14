from fastapi import FastAPI
from base64 import b64encode
import json

from app.router import router
from app.service.timetable import Comci
from app.service.meal import Neis

tt = Comci()
meal = Neis()

app = FastAPI(
    title="Classfood Timetable API",
    description="학교 급식 및 시간표 API",
    version="0.0.1",
)

@app.get("/api/search")
async def search_school(school_name_comci: str, school_name_neis: str = None): # type: ignore
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

app.include_router(router)