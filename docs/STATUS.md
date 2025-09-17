When paused: Sep 17, 2025 (America/Chicago)
Branch: feature/api → PR open into main
Auth: SSH push working

✅ Done

Repo structure fixed (.github/workflows/, api/, infra/, ops/, Dockerfile, pytest.ini).

SSH key created (WSL), remote switched to SSH, pushes working.

PR from feature/api → main opened.

Workflows added:

ci.yml (runs on PRs to main and pushes to feature/**).

cd.yml scoped to main and manual (Terraform/CD parked for now).

🔴 Current issue (CI failing)

CI triggers correctly but fails during test/build phase.

Likely causes on first run: dependency mismatch for TestClient and/or pytest discovery.

🎯 Next actions (when you’re back)

Stabilize tests & deps

Replace api/requirements.txt with pinned, known-good versions:

fastapi==0.110.0
starlette==0.37.2
uvicorn[standard]==0.29.0
gunicorn==21.2.0
httpx==0.27.2


Ensure a minimal passing test exists:
api/tests/test_app.py

from starlette.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"ok": True}


Make sure pytest finds tests:
pytest.ini

[pytest]
testpaths = api/tests
pythonpath = .


Commit & push:

git add api/requirements.txt api/tests/test_app.py pytest.ini
git commit -m "ci: pin deps and stabilize tests"
git push


Watch Actions → CI. If red, open the failing job and copy the last 20 lines of the failing step.

(After CI is green) Enable CD step-by-step

Create AWS ECR repo (cloud-api), S3+DynDB for TF backend.

Set up GitHub→AWS OIDC IAM role (no long-lived keys).

Update cd.yml to:

terraform init/plan on PRs,

apply + ECS deploy on main.

Add repo secret AWS_ACCOUNT_ID and wire aws-actions/configure-aws-credentials.

🧭 Quick “where am I?” commands (when you sit back down)
git status
git branch -vv
git log --oneline --decorate -n 5
ls -R .github/workflows
cat api/requirements.txt

✅ Definition of “CI green” for this project

Workflow runs on PR and on pushes to feature branches.

Steps pass: checkout → set up Python → install deps → pytest -q → Docker image build (no push yet).

📌 Notes

cd.yml is intentionally limited to main/manual to avoid Terraform init errors until AWS bits exist.

Once CI is green, we’ll do OIDC + ECR, then ECS Fargate deploy with Terraform.