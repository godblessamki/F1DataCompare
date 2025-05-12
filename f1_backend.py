# f1_backend.py
import fastf1
from typing import Tuple, List, Union

fastf1.Cache.enable_cache("cache")

ALLOWED_DRIVERS = {"VER": "Verstappen", "LEC": "Leclerc"}
AVAILABLE_STATS = ["Lap Time", "Sector 1", "Sector 2", "Sector 3", "Tyre Compound"]

def get_completed_2025_races() -> List[str]:
    races = []
    for round_number in range(1, 25):  # estimate max number of races
        try:
            session = fastf1.get_session(2025, round_number, "R")
            session.load()
            races.append(session.event["EventName"])
        except Exception:
            continue
    return races

def get_driver_stat(year: int, grand_prix: str, driver_code: str, stat: str) -> Tuple[List[int], List[Union[float, str]], str]:
    if driver_code not in ALLOWED_DRIVERS:
        return [], [], f"Driver {driver_code} is not supported."
    
    try:
        session = fastf1.get_session(year, grand_prix, "R")
        session.load()
        laps = session.laps.pick_driver(driver_code)

        if laps.empty:
            return [], [], f"No laps found for {driver_code} – {grand_prix}"
        
        lap_numbers = laps["LapNumber"].tolist()

        if stat == "Lap Time":
            data = [lt.total_seconds() if lt is not None else None for lt in laps["LapTime"]]
        elif stat == "Sector 1":
            data = [t.total_seconds() if t is not None else None for t in laps["Sector1Time"]]
        elif stat == "Sector 2":
            data = [t.total_seconds() if t is not None else None for t in laps["Sector2Time"]]
        elif stat == "Sector 3":
            data = [t.total_seconds() if t is not None else None for t in laps["Sector3Time"]]
        elif stat == "Tyre Compound":
            data = laps["Compound"].tolist()
        else:
            return [], [], "Unsupported stat"

        name = ALLOWED_DRIVERS[driver_code]
        return lap_numbers[:len(data)], data, f"{name} – {grand_prix} GP ({stat})"

    except Exception as e:
        return [], [], f"Error: {str(e)}"
