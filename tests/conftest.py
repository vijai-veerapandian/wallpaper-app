import json
import pytest
from app import create_app


@pytest.fixture
def sample_schedule():
    return {
        "slots": {
            "morning": {
                "start": "06:00",
                "end": "11:59",
                "rotation_seconds": 15,
                "wallpapers": [
                    "morning/daniel-leone-g30P1zcOzXo-unsplash.jpg",
                    "morning/kalen-emsley-Bkci_8qcdvQ-unsplash.jpg",
                ],
            },
            "afternoon": {
                "start": "12:00",
                "end": "16:59",
                "rotation_seconds": 15,
                "wallpapers": [
                    "afternoon/philipp-upR8raSXvwg-unsplash.jpg",
                    "afternoon/yousef-espanioly-g1vMcIdygUU-unsplash.jpg",
                ],
            },
            "evening": {
                "start": "17:00",
                "end": "20:59",
                "rotation_seconds": 20,
                "wallpapers": [
                    "evening/jason-mavrommatis-GPPAjJicemU-unsplash.jpg",
                    "evening/quino-al-mBQIfKlvowM-unsplash.jpg",
                ],
            },
            "night": {
                "start": "21:00",
                "end": "05:59",
                "rotation_seconds": 30,
                "wallpapers": [
                    "night/johannes-plenio-DKix6Un55mw-unsplash.jpg",
                    "night/nathan-anderson-L95xDkSSuWw-unsplash.jpg",
                ],
            },
        }
    }


@pytest.fixture
def app(tmp_path, sample_schedule):
    schedule_file = tmp_path / "schedule.json"
    schedule_file.write_text(json.dumps(sample_schedule))

    app = create_app(
        {
            "TESTING": True,
            "SCHEDULE_FILE": str(schedule_file),
        }
    )

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
