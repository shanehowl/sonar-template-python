#!/usr/bin/env bash
# Lint, test with coverage, then scan with the local SonarQube and wait for the quality gate.
# Usage: SONAR_TOKEN=<project analysis token> scripts/scan.sh   (or put it in .env)
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

export SONAR_HOST_URL="${SONAR_HOST_URL:-http://localhost:9000}"
: "${SONAR_TOKEN:?Set SONAR_TOKEN (in your shell or .env) to a project analysis token}"

curl -fsS "${SONAR_HOST_URL}/api/system/status" | grep -q '"status":"UP"' || {
  echo "ERROR: SonarQube is not UP at ${SONAR_HOST_URL}. Start it first." >&2
  exit 1
}

echo "==> ruff"
uv run ruff check .
uv run ruff format --check .

echo "==> pytest + coverage"
uv run pytest

echo "==> pysonar -> ${SONAR_HOST_URL}"
# Reads [tool.sonar] in pyproject.toml; SONAR_HOST_URL and SONAR_TOKEN come from the environment.
# Exits non-zero if the quality gate fails (sonar.qualitygate.wait=true).
uv run pysonar
