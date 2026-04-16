def create_user_and_login(client):
    client.post("/api/v1/register", json={
        "email": "test@test.com",
        "password": "123456"
    })

    response = client.post("/api/v1/login", json={
        "email": "test@test.com",
        "password": "123456"
    })

    return response.json()["access_token"]


def test_create_and_get_habits(client):
    token = create_user_and_login(client)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post(
        "/api/v1/habits",
        json={"title": "leer"},
        headers=headers
    )

    assert response.status_code == 200

    response = client.get(
        "/api/v1/habits",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_complete_and_delete_habit(client):
    token = create_user_and_login(client)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post(
        "/api/v1/habits",
        json={"title": "entrenar"},
        headers=headers
    )

    assert response.status_code == 200

    response = client.get("/api/v1/habits", headers=headers)
    habit_id = response.json()[0]["id"]

    response = client.patch(
        f"/api/v1/habits/{habit_id}",
        headers=headers
    )

    assert response.json()["completed"] == True

    response = client.delete(
        f"/api/v1/habits/{habit_id}",
        headers=headers
    )

    assert response.status_code == 200