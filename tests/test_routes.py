def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_index_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Active slot" in response.data


def test_settings_page_loads(client):
    response = client.get("/settings")
    assert response.status_code == 200
    assert b"Wallpaper Schedule Settings" in response.data


def test_api_current_returns_expected_shape(client):
    response = client.get("/api/current")
    data = response.get_json()

    assert response.status_code == 200
    assert "active_slot" in data
    assert "rotation_seconds" in data
    assert "wallpapers" in data


def test_settings_post_updates_schedule(client, app):
    response = client.post(
        "/settings",
        data={
            "morning_start": "05:30",
            "morning_end": "11:30",
            "morning_rotation_seconds": "10",
            "morning_wallpapers": "morning/a.jpg\nmorning/b.jpg",
            "afternoon_start": "12:00",
            "afternoon_end": "16:59",
            "afternoon_rotation_seconds": "20",
            "afternoon_wallpapers": "afternoon/c.jpg",
            "evening_start": "17:00",
            "evening_end": "20:59",
            "evening_rotation_seconds": "25",
            "evening_wallpapers": "evening/d.jpg",
            "night_start": "21:00",
            "night_end": "05:59",
            "night_rotation_seconds": "30",
            "night_wallpapers": "night/e.jpg",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Wallpaper Schedule Settings" in response.data
