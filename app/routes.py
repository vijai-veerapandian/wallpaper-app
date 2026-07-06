from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .services import load_schedule, save_schedule, get_active_slot

main = Blueprint("main", __name__)


@main.route("/")
def index():
    schedule = load_schedule()
    slot_name, slot_data = get_active_slot(schedule)
    wallpapers = slot_data["wallpapers"] if slot_data else []
    rotation_seconds = slot_data["rotation_seconds"] if slot_data else 30

    return render_template(
        "index.html",
        active_slot=slot_name,
        wallpapers=wallpapers,
        rotation_seconds=rotation_seconds,
    )


@main.route("/settings", methods=["GET", "POST"])
def settings():
    schedule = load_schedule()

    if request.method == "POST":
        for slot_name in schedule["slots"]:
            schedule["slots"][slot_name]["start"] = request.form.get(f"{slot_name}_start")
            schedule["slots"][slot_name]["end"] = request.form.get(f"{slot_name}_end")
            schedule["slots"][slot_name]["rotation_seconds"] = int(
                request.form.get(f"{slot_name}_rotation_seconds")
            )

            wallpapers_raw = request.form.get(f"{slot_name}_wallpapers", "")
            schedule["slots"][slot_name]["wallpapers"] = [
                line.strip() for line in wallpapers_raw.splitlines() if line.strip()
            ]

        save_schedule(schedule)
        return redirect(url_for("main.settings"))

    return render_template("settings.html", schedule=schedule)


@main.route("/api/current")
def current_wallpaper():
    schedule = load_schedule()
    slot_name, slot_data = get_active_slot(schedule)

    return jsonify(
        {
            "active_slot": slot_name,
            "rotation_seconds": slot_data["rotation_seconds"] if slot_data else 30,
            "wallpapers": slot_data["wallpapers"] if slot_data else [],
        }
    )


@main.route("/health")
def health():
    return jsonify({"status": "ok"})
