import json
from datetime import datetime
from pathlib import Path
from flask import current_app

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SCHEDULE_FILE = BASE_DIR / "config" / "schedule.json"


def get_schedule_file():
    if current_app and current_app.config.get("SCHEDULE_FILE"):
        return Path(current_app.config["SCHEDULE_FILE"])
    return DEFAULT_SCHEDULE_FILE


def load_schedule():
    schedule_file = get_schedule_file()
    with open(schedule_file, "r") as f:
        return json.load(f)


def save_schedule(data):
    schedule_file = get_schedule_file()
    with open(schedule_file, "w") as f:
        json.dump(data, f, indent=2)


def time_in_range(start_str, end_str, current_str):
    start = datetime.strptime(start_str, "%H:%M").time()
    end = datetime.strptime(end_str, "%H:%M").time()
    current = datetime.strptime(current_str, "%H:%M").time()

    if start <= end:
        return start <= current <= end
    return current >= start or current <= end


def get_active_slot(schedule):
    now = datetime.now().strftime("%H:%M")
    for slot_name, slot_data in schedule["slots"].items():
        if time_in_range(slot_data["start"], slot_data["end"], now):
            return slot_name, slot_data
    return None, None
