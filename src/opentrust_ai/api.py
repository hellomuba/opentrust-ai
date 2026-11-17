"""Optional localhost demonstration API. No accounts or remote testing support."""

from fastapi import FastAPI

from .assessment import AssessmentRunner

app = FastAPI(
    title="OpenTrust AI (synthetic demo)",
    version="0.1.0",
    description="Experimental, unauthenticated localhost-only demo. Do not expose publicly.",
)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/assessments/demo")
def run_demo() -> dict:
    """Runs only fixed synthetic scenarios; accepts no target URLs or credentials."""
    return AssessmentRunner().run().to_dict()
