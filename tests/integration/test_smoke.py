"""Integration tests for tracer-bullet - real HTTP calls against a running
instance (ephemeral PR-preview namespace, staging, or a local port-forward
for development). Unlike tests/unit's in-process TestClient, these never
mock the HTTP layer - the whole point is proving the deployed service
actually answers over the network.

Target is TRACER_BULLET_BASE_URL, not a hardcoded host, so the same suite
runs unchanged against any environment. Defaults to a local port-forward
(`kubectl port-forward svc/tracer-bullet 18000:80` then
`TRACER_BULLET_BASE_URL=http://localhost:18000` - or omit the env var to
match this default directly).
"""

import json
import os
import urllib.error
import urllib.request

import pytest

BASE_URL = os.environ.get("TRACER_BULLET_BASE_URL", "http://localhost:18000")


def _get(path: str) -> tuple[int, dict]:
    url = f"{BASE_URL}{path}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


@pytest.mark.integration
def test_root_is_reachable():
    status, body = _get("/")
    assert status == 200
    assert body["message"] == "Hello from the tracer bullet!"


@pytest.mark.integration
def test_health_is_reachable():
    status, body = _get("/health")
    assert status == 200
    assert body["status"] == "ok"
