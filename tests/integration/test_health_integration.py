from wsgi import app


def test_health_responde_200():
    response = app.test_client().get("/health")
    assert response.status_code == 200
