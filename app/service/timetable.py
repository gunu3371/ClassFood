from pycomcigan import TimeTable, get_school_code
from datetime import datetime
from pprint import pprint


class Comci:
    def __init__(self) -> None:
        pass

    def search_school(self, school_name):
        return get_school_code(school_name)

    def get(self, school_name, local_code, school_code, grade, class_, date):
        if school_code is not None:
            timetable = TimeTable(school_name, local_code, school_code, week_num=0)
        else:
            timetable = TimeTable(school_name, week_num=0)

        return self._to_dict(timetable.timetable[grade][class_][self._get_week(date)])

    def _to_dict(self, timetable):
        ret = []
        for i in timetable:
            if (
                (i.subject == "" and i.teacher == "")
                and (i.replaced is False)
                and (i.original is None)
            ):
                continue
            ret.append(
                {
                    "period": i.period,
                    "subject": i.subject,
                    "teacher": i.teacher,
                    "replaced": i.replaced,
                    "original": (
                        {
                            "period": i.original.period if i.original else None,
                            "subject": i.original.subject if i.original else None,
                            "teacher": i.original.teacher if i.original else None,
                        }
                        if i.original
                        else None
                    ),
                }
            )
        return ret

    def _get_week(self, _datetime):
        today = _datetime.weekday()
        weekday_mapping = {
            0: TimeTable.MONDAY,
            1: TimeTable.TUESDAY,
            2: TimeTable.WEDNESDAY,
            3: TimeTable.THURSDAY,
            4: TimeTable.FRIDAY,
        }
        try:
            return weekday_mapping.get(today)
        except KeyError:
            return None


class Neis:
    def __init__(self) -> None:
        pass


if __name__ == "__main__":
    comci = Comci()
    school = comci.search_school("선린인")[0]
    print(school)
    pprint(comci.get(school[2], 1, 10, datetime.now(), school[3]))
