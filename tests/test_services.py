from app.services import load_schedule, save_schedule, time_in_range, get_active_slot


def test_load_schedule(app, sample_schedule):
    with app.app_context():
        loaded = load_schedule()
        assert loaded == sample_schedule


def test_save_schedule(app, sample_schedule):
    sample_schedule["slots"]["morning"]["rotation_seconds"] = 99

    with app.app_context():
        save_schedule(sample_schedule)
        loaded = load_schedule()

    assert loaded["slots"]["morning"]["rotation_seconds"] == 99


def test_time_in_range_normal_window():
    assert time_in_range("06:00", "11:59", "08:30") is True
    assert time_in_range("06:00", "11:59", "12:30") is False


def test_time_in_range_wraparound_window():
    assert time_in_range("21:00", "05:59", "23:00") is True
    assert time_in_range("21:00", "05:59", "03:00") is True
    assert time_in_range("21:00", "05:59", "14:00") is False


def test_get_active_slot_returns_slot(monkeypatch):
    schedule = {
        "slots": {
            "morning": {
                "start": "06:00",
                "end": "11:59",
                "rotation_seconds": 15,
                "wallpapers": ["morning/a.jpg"],
            },
            "night": {
                "start": "21:00",
                "end": "05:59",
                "rotation_seconds": 30,
                "wallpapers": ["night/b.jpg"],
            },
        }
    }

    from app import services

    class FakeDateTime:
        @classmethod
        def now(cls):
            class FakeNow:
                def strftime(self, fmt):
                    return "07:30"

            return FakeNow()

        @classmethod
        def strptime(cls, value, fmt):
            from datetime import datetime

            return datetime.strptime(value, fmt)

    monkeypatch.setattr(services, "datetime", FakeDateTime)

    slot_name, slot_data = get_active_slot(schedule)

    assert slot_name == "morning"
    assert slot_data["wallpapers"] == ["morning/a.jpg"]
