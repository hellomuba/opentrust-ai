import json

from fastapi.testclient import TestClient

from opentrust_ai.api import app
from opentrust_ai.cli import main


def test_cli_json(capsys):
    assert main(["demo", "--format", "json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["summary"]["passed"] == 4


def test_cli_writes_report(tmp_path):
    output = tmp_path / "report.json"
    assert main(["demo", "--format", "json", "--output", str(output)]) == 0
    assert json.loads(output.read_text())["summary"]["failed"] == 0


def test_api_health_and_fixed_demo():
    client = TestClient(app)
    assert client.get("/healthz").json() == {"status": "ok"}
    response = client.post("/v1/assessments/demo")
    assert response.status_code == 200
    assert response.json()["summary"]["passed"] == 4


def test_api_does_not_expose_generic_url_scanning():
    client = TestClient(app)
    assert client.post("/v1/assessments", json={"target_url": "https://example.com"}).status_code == 404
