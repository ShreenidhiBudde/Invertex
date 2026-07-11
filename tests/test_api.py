import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from search_engine.api.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_search_returns_200(client):
    response = client.get("/search", params={"q": "python list append", "k": 5})
    assert response.status_code == 200


def test_search_response_shape(client):
    response = client.get("/search", params={"q": "python list append", "k": 5})
    data = response.json()

    assert "query" in data
    assert "results" in data
    assert "latency_ms" in data
    assert isinstance(data["results"], list)


def test_search_result_fields(client):
    response = client.get("/search", params={"q": "python list append", "k": 5})
    data = response.json()

    assert len(data["results"]) > 0
    first = data["results"][0]
    assert "doc_id" in first
    assert "score" in first
    assert "title" in first
    assert "snippet" in first


def test_search_respects_k(client):
    response = client.get("/search", params={"q": "python", "k": 3})
    data = response.json()
    assert len(data["results"]) <= 3


def test_search_nonsense_query_returns_empty_or_ok(client):
    response = client.get("/search", params={"q": "zzzznonexistentqueryterm", "k": 5})
    assert response.status_code == 200