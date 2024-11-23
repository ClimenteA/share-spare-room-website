from datetime import datetime
from pytz import timezone


months = {
    1: "Ianuarie",
    2: "Februarie",
    3: "Martie",
    4: "Aprilie",
    5: "Mai",
    6: "Iunie",
    7: "Iulie",
    8: "August",
    9: "Septembrie",
    10: "Octombrie",
    11: "Noiembrie",
    12: "Decembrie",
}


def convert_to_ro_date(iso_date: str):
    dt = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S.%f")

    ro_tz = timezone("Europe/Bucharest")
    ro_datetime = dt.astimezone(ro_tz)

    formatted_date = f"{ro_datetime.day} {months[ro_datetime.month]} {ro_datetime.hour:02d}:{ro_datetime.minute:02d}"

    return formatted_date
