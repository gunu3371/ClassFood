from neispy import Neispy
from asyncio.events import get_event_loop
from pprint import pprint

class Neis:
    def __init__(self):
        self.neis = Neispy()

    def close(self):
        pass

    async def get(self, region_code, school_code, date):
        m = await self.neis.mealServiceDietInfo(ATPT_OFCDC_SC_CODE=region_code, SD_SCHUL_CODE=school_code, MLSV_YMD=date.strftime("%Y%m%d"))
        return m.mealServiceDietInfo[1].row[0]

    async def search_school(self, school_name):
        s = await self.neis.schoolInfo(SCHUL_NM=school_name)
        return s.schoolInfo[1].row

if __name__ == "__main__":
    async def main():
        meal=Neis()
        schools = await meal.search_school("선린")
        pprint(schools)


    get_event_loop().run_until_complete(main())
