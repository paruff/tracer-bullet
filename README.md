# python-fawkes-path

A deliberately minimal FastAPI service. It is **not** a Fawkes product feature — it exists to be run through the Fawkes Internal Developer Platform's full pipeline (CI build/lint/scan/test, GitOps continuous delivery, and observability) so the platform's own machinery can be validated end-to-end against a real, tiny, disposable example.

Desired-state Kubernetes manifests for this service live in a separate repo: [paruff/python-fawkes-path-gitops](https://github.com/paruff/python-fawkes-path-gitops), synced by ArgoCD.

## Endpoints
- `GET /` — hello-world response with the running version
- `GET /health`, `GET /ready` — liveness/readiness
- `GET /info` — service metadata
- `GET /metrics` — Prometheus metrics
- `GET /demo/span` — emits a sample OpenTelemetry trace span

## Local development
```
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
pytest tests/unit
```

## CI/CD
Built and validated via [Tekton](https://tekton.dev) Pipelines running in the Fawkes cluster (see [paruff/fawkes#1659](https://github.com/paruff/fawkes/issues/1659) and related issues), not GitHub Actions. On a successful build, the pipeline opens a PR against [paruff/python-fawkes-path-gitops](https://github.com/paruff/python-fawkes-path-gitops) to bump the deployed image tag; ArgoCD syncs it to the cluster.
